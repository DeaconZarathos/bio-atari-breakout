import time
import ale_py
import gymnasium as gym
import keyboard
import cl  # SDK oficial de Cortical Labs

# Registrar explícitamente los entornos de ALE para Gymnasium
gym.register_envs(ale_py)

def extract_game_state(env):
    """Extrae las coordenadas y estado de la RAM del emulador de Atari Breakout."""
    ram = env.unwrapped.ale.getRAM()
    ball_x = int(ram[99])
    paddle_x = int(ram[72])
    ball_y = int(ram[101]) if len(ram) > 101 else 0
    return {"paddle_x": paddle_x, "ball_x": ball_x, "ball_y": ball_y}

def run_directional_breakout():
    env = gym.make("ALE/Breakout-v5", render_mode="human")
    print("Iniciando entorno con control de dirección vertical (Y) y zonas relativas...")
    print("CONTROLES: Presiona [ESPACIO] para sacar la pelota (FIRE).")
    
    with cl.open() as neurons:
        num_episodes = 3
        
        for episode in range(num_episodes):
            observation, info = env.reset()
            terminated = False
            truncated = False
            
            print(f"\n--- Iniciando Episodio {episode + 1} ---")
            
            # Saque inicial automático
            for _ in range(10):
                env.step(1)
                time.sleep(0.01)
            
            # Inicializar posición previa de Y para calcular la dirección
            initial_state = extract_game_state(env)
            prev_ball_y = initial_state["ball_y"]
            
            frame_count = 0
            
            while not terminated and not truncated:
                state = extract_game_state(env)
                ball_x = state["ball_x"]
                paddle_x = state["paddle_x"]
                ball_y = state["ball_y"]
                delta_x = ball_x - paddle_x
                
                # Calcular la dirección vertical (Delta Y)
                # En Atari Y aumenta hacia abajo: positivo = bajando, negativo = subiendo
                ball_dy = ball_y - prev_ball_y
                is_descending = ball_dy > 0
                
                # 1. ENTRADA (Sensorial): Considera posición horizontal y dirección vertical
                channels = []
                try:
                    # Solo estimulamos activamente si la pelota está en juego y bajando hacia la paleta
                    if 0 < ball_y < 200:
                        rel_pos = ball_x - paddle_x  # Distancia horizontal
                        
                        if rel_pos < -15:
                            channels = [1, 2, 3, 4]       # Lejos a la Izquierda
                        elif -15 <= rel_pos < -3:
                            channels = [5, 6, 7, 8]       # Cerca a la Izquierda
                        elif -3 <= rel_pos <= 3:
                            channels = [6, 7, 10, 11]     # CENTRO (Neutral)
                        elif 3 < rel_pos <= 15:
                            channels = [9, 10, 11, 12]    # Cerca a la Derecha
                        else:
                            channels = [13, 14, 15, 16]   # Lejos a la Derecha
                            
                        # Si la pelota viene bajando, duplicamos el estímulo para darle más peso al "peligro inminente"
                        neurons.stim(channels=channels)
                        if is_descending:
                            neurons.stim(channels=channels) 
                    else:
                        channels = []  # Sin estímulo si no hay pelota activa
                except Exception as e:
                    pass

                # Actualizar la posición previa de Y para el siguiente ciclo
                prev_ball_y = ball_y

                # 2. SALIDA (Decodificación de Spikes)
                spikes_left = 0
                spikes_right = 0
                
                try:
                    spike_data = neurons.read()
                    if spike_data is not None:
                        if isinstance(spike_data, (list, tuple, set)):
                            for item in spike_data:
                                ch = int(item) if isinstance(item, (int, float)) else getattr(item, 'channel', None)
                                if ch is not None:
                                    if 1 <= ch <= 8: spikes_left += 1
                                    elif 9 <= ch <= 16: spikes_right += 1
                        elif isinstance(spike_data, dict):
                            for ch_key, val in spike_data.items():
                                ch = int(ch_key)
                                if val > 0:
                                    if 1 <= ch <= 8: spikes_left += val
                                    elif 9 <= ch <= 16: spikes_right += val
                except Exception as e:
                    pass

                # 3. DECISIÓN: Control neuronal con respaldo de seguimiento inteligente
                if spikes_right > spikes_left:
                    action = 2  # Derecha ordenada por la red
                    source = "NEURONAL -> DERECHA"
                elif spikes_left > spikes_right:
                    action = 3  # Izquierda ordenada por la red
                    source = "NEURONAL -> IZQUIERDA"
                else:
                    # Respaldo inteligente para mantener la fluidez del juego
                    if delta_x > 2:
                        action = 2
                        source = "RESPALDO -> DERECHA"
                    elif delta_x < -2:
                        action = 3
                        source = "RESPALDO -> IZQUIERDA"
                    else:
                        action = 0
                        source = "RESPALDO -> CENTRO"

                # Intervención manual de emergencia por teclado
                if keyboard.is_pressed('space'):
                    action = 1
                    source = "MANUAL -> FIRE"
                elif keyboard.is_pressed('left'):
                    action = 3
                    source = "MANUAL -> IZQUIERDA"
                elif keyboard.is_pressed('right'):
                    action = 2
                    source = "MANUAL -> DERECHA"
                
                # Ejecutar acción en el emulador
                observation, reward, terminated, truncated, info = env.step(action)
                
                # 4. REFORZAMIENTO (Feedback Loop): GOLPE vs FALLO
                if reward > 0:
                    try:
                        neurons.stim(channels=list(range(1, 17)))  # Premio masivo
                    except:
                        pass
                elif state["ball_y"] > 190:
                    try:
                        neurons.stim(channels=[7, 8, 9, 10])     # Castigo central
                    except:
                        pass

                # 5. Monitoreo en consola incluyendo la dirección vertical
                frame_count += 1
                if frame_count % 30 == 0:
                    dir_str = "BAJANDO ⬇️" if is_descending else "SUBIENDO ⬆️"
                    print(f"[Frame {frame_count}] DirY: {dir_str} | RelPos: {delta_x:3d} | Canales: {channels if channels else 'INACTIVOS'}")

                time.sleep(0.016)

    env.close()
    print("Sesión finalizada.")

if __name__ == "__main__":
    run_directional_breakout()