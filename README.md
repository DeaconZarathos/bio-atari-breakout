# 🧠 Bio-Hybrid Atari Breakout Client (CL-SDK & Gymnasium)

[![DOI](https://zenodo.org/badge/1445106786.svg)](https://doi.org/10.5281/zenodo.23936588)

Este repositorio contiene un adelanto funcional de un **sistema de control híbrido bio-digital** que conecta el hardware biológico (neuronas en chip/DishBrain) de **Cortical Labs** con el entorno de simulación **Gymnasium (Atari 2600 Breakout)**. 

El proyecto implementa un bucle de circuito cerrado (*closed-loop*) donde un cultivo celular vivo interactúa con un videojuego en tiempo real mediante estímulos vectoriales y decodificación de impulsos eléctricos (*spikes*).

---

## 🚀 Características del Adelanto

*   **Lectura Directa de RAM:** Extracción optimizada de las coordenadas exactas de la pelota y la paleta leyendo directamente la memoria del emulador Atari (`ALE-Py`), evitando el retraso del procesamiento de imágenes.
*   **Mitigación de Fatiga Celular:** El sistema restringe y modula la estimulación sensorial basándose en el vector de movimiento vertical de la pelota. Las neuronas solo reciben estímulos cuando la pelota está descendiendo, optimizando el ancho de banda biológico y evitando la saturación del tejido.
*   **Arquitectura de Control Tri-Capa (Co-Pilotaje):** 
    1.  *Prioridad Neuronal:* Decodificación en tiempo real de los canales motores biológicos.
    2.  *Respaldo Algorítmico:* Sistema de seguimiento automatizado de emergencia para mantener la fluidez del juego si las neuronas están en periodo de descanso.
    3.  *Intervención Manual:* Control humano directo por teclado para propósitos de entrenamiento guiado o saques (`FIRE`).
*   **Bucle de Reforzamiento:** Estímulos de recompensa masiva coordinada ante ganancias de puntuación y estímulos disruptivos de advertencia en zonas críticas inferiores.

---

## 🛠️ Requisitos e Instalación

Para ejecutar este script, asegúrate de contar con Python 3.9+ y las dependencias del entorno:

```bash
pip install gymnasium[atari] ale-py keyboard numpy
```

> ⚠️ **Nota sobre el Hardware:** Este script requiere acceso al SDK oficial de **Cortical Labs** (`import cl`). Si no dispones de una cuenta de desarrollador activa o hardware DishBrain conectado, el script fallará en la inicialización del módulo `cl`.

---

## 📂 Estructura del Código Principal

El script ejecuta un bucle continuo a **60 FPS** simulados (~16ms por frame) dividiéndose en 5 etapas críticas:
1.  **Extracción del estado:** Monitoreo horizontal y vertical de la física del juego.
2.  **Codificación Sensorial:** Mapeo de la distancia relativa (`delta_x`) en 5 zonas de electrodos.
3.  **Decodificación de Spikes:** Conteo diferencial de impulsos en canales izquierdos (1-8) y derechos (9-16).
4.  **Toma de Decisiones:** Ejecución de la acción en el entorno mediante prioridades híbridas.
5.  **Reforzamiento:** Emisión de descargas eléctricas adaptativas según el éxito o fracaso del frame.

---

## 📈 Próximos Pasos (Roadmap del Proyecto)
*   [ ] Implementar un sistema de telemetría automatizado que exporte la actividad bioeléctrica a archivos `.csv`.
*   [ ] Diseñar un modo de control puramente biológico (aislando por completo el algoritmo de respaldo) para medir curvas de aprendizaje estadístico.
*   [ ] Migrar el bucle de ejecución síncrono a una arquitectura asíncrona (`asyncio`) para mejorar la precisión de muestreo del SDK.

---

## 🤝 Contribuciones y Comunidad
Este es un proyecto de código abierto en fase de desarrollo temprano. Si eres parte de la comunidad de **Cortical Labs**, neurocientífico computacional o entusiasta de la *Organoid Intelligence*, ¡tus ideas son bienvenidas! Siente libertad de abrir un *Issue* o enviar un *Pull Request*.
