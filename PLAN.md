# Plan de Trabajo - Proyecto 2 IA (Knight Energy)

> **Proyecto:** Knight Energy - Inteligencia Artificial\
> **Duración estimada:** 2 a 3 días\
> **Equipo:** Perea, Manuel, Allan

------------------------------------------------------------------------
# Descripción del Proyecto

## Contexto

El presente proyecto consiste en desarrollar **Knight Energy**, un juego de estrategia por turnos para dos jugadores basado en el movimiento del caballo del ajedrez. El objetivo principal es aplicar conceptos de Inteligencia Artificial mediante la implementación del algoritmo **Minimax con decisiones imperfectas**, permitiendo que la máquina tome decisiones estratégicas según diferentes niveles de dificultad.

En el juego, cada jugador controla un caballo sobre un tablero de ajedrez que contiene casillas con puntos y casillas especiales de recuperación de energía. Cada movimiento consume energía y el jugador debe administrar cuidadosamente este recurso mientras busca maximizar la cantidad de puntos obtenidos antes de que finalice la partida.

El juego inicia con la máquina realizando el primer movimiento. Durante cada turno, ambos jugadores pueden desplazarse siguiendo el movimiento en "L" característico del caballo en ajedrez. Al visitar una casilla con puntos o energía, esta desaparece del tablero y no podrá volver a ser utilizada por ninguno de los jugadores.

La inteligencia artificial deberá utilizar el algoritmo **Minimax** con una profundidad de búsqueda configurable según el nivel de dificultad seleccionado por el usuario:

- **Principiante:** profundidad 2
- **Amateur:** profundidad 4
- **Experto:** profundidad 6

Además del desarrollo del videojuego, el proyecto requiere documentar la función heurística utilizada para evaluar los estados del juego, justificando los criterios empleados por la inteligencia artificial para seleccionar la mejor jugada.

---

## Objetivo General

Desarrollar una aplicación que implemente el juego **Knight Energy**, integrando una interfaz gráfica, la lógica completa del juego y un agente inteligente basado en el algoritmo Minimax, capaz de competir contra el usuario en distintos niveles de dificultad.

---

## Objetivos Específicos

- Implementar la lógica completa del juego respetando las reglas establecidas.
- Diseñar una interfaz gráfica clara e intuitiva para la interacción con el usuario.
- Desarrollar un agente inteligente utilizando el algoritmo Minimax.
- Diseñar una función heurística que permita evaluar adecuadamente los estados del juego.
- Integrar todos los componentes en una aplicación funcional y correctamente documentada.

---

# Objetivo

Desarrollar el proyecto de forma paralela para minimizar bloqueos entre
los integrantes, dejando la integración para el segundo día.

------------------------------------------------------------------------

# Distribución General

  Integrante   Responsabilidad Principal
  ------------ ---------------------------
  **Perea**    Lógica del juego (Core)
  **Manuel**   Interfaz gráfica
  **Allan**    IA (Minimax + Heurística)

------------------------------------------------------------------------

# Día 1 --- Desarrollo Paralelo

## Tarea 1 --- Modelo del Juego

**Encargado:** Perea

### Objetivo

Implementar toda la lógica independiente de la interfaz.

### Incluye

-   Representación del tablero
-   Estado del juego (`GameState`)
-   Jugadores
-   Movimiento del caballo
-   Reglas del ajedrez para el caballo
-   Casillas de puntos
-   Casillas de energía
-   Consumo y recuperación de energía
-   Obtención de puntos
-   Eliminación de casillas consumidas
-   Generación aleatoria del tablero
-   Condiciones de finalización
-   Determinación del ganador

### Entregable

`GameState` completamente funcional.

------------------------------------------------------------------------

## Tarea 2 --- Interfaz Gráfica

**Encargado:** Manuel

### Objetivo

Construir toda la interfaz utilizando datos simulados (Mock Data).

### Incluye

-   Ventana principal
-   Tablero
-   Renderizado de piezas
-   Indicador de turno
-   Marcador de puntos
-   Indicador de energía
-   Selector de dificultad
-   Botón Nuevo Juego
-   Pantalla de ganador

### Dependencias

Ninguna.

------------------------------------------------------------------------

## Tarea 3 --- IA (Minimax)

**Encargado:** Allan

### Objetivo

Desarrollar el algoritmo Minimax de forma independiente.

### Incluye

-   Árbol de búsqueda
-   Generación de hijos
-   Minimax
-   Profundidad configurable
-   Función heurística
-   Selección del mejor movimiento

### Dependencias

Ninguna (puede trabajar con un estado simplificado).

------------------------------------------------------------------------

# Día 2 --- Integración

## Tarea 4 --- Conectar la GUI con la lógica

**Encargado:** Manuel

### Depende de

-   **Tarea 1 --- Perea**

------------------------------------------------------------------------

## Tarea 5 --- Integrar Minimax con el juego

**Encargado:** Allan

### Depende de

-   **Tarea 1 --- Perea**

------------------------------------------------------------------------

## Tarea 6 --- Turnos de la máquina

**Encargado:** Allan

### Incluye

-   La máquina inicia la partida
-   Cambio de turnos
-   Selección de profundidad según dificultad

### Depende de

-   **Tarea 5 --- Allan**

------------------------------------------------------------------------

## Tarea 7 --- Soporte e integración

**Encargado:** Perea

Mientras Manuel y Allan integran:

-   Corrección de bugs
-   Ajustes al GameState
-   Funciones auxiliares
-   Apoyo en integración

------------------------------------------------------------------------

# Día 3 --- Pruebas y Entrega

## Tarea 8 --- Testing

**Encargados:** Todos

### Casos de prueba

-   Movimiento válido del caballo
-   Consumo de energía
-   Recuperación de energía
-   Recolección de puntos
-   Casillas consumidas
-   Sin energía
-   Fin del juego
-   Empate
-   Profundidad 2
-   Profundidad 4
-   Profundidad 6

------------------------------------------------------------------------

## Tarea 9 --- Informe

**Encargado:** Perea

### Contenido

-   Explicación de la heurística
-   Función de utilidad
-   Funcionamiento del algoritmo
-   Justificación de la evaluación de estados

------------------------------------------------------------------------

# Dependencias

  Nº   Tarea                    Encargado   Depende de
  ---- ------------------------ ----------- ---------------------
  1    Modelo del juego         Perea       ---
  2    Interfaz gráfica         Manuel      ---
  3    Minimax base             Allan       ---
  4    Integración GUI          Manuel      **Tarea 1 (Perea)**
  5    Integración Minimax      Allan       **Tarea 1 (Perea)**
  6    Turnos de la máquina     Allan       **Tarea 5 (Allan)**
  7    Correcciones y soporte   Perea       Durante integración
  8    Testing                  Todos       Tareas 4, 5 y 6
  9    Informe                  Perea       Proyecto finalizado

------------------------------------------------------------------------

# Arquitectura Propuesta

``` text
project/
│
├── game/
│   ├── GameState
│   ├── Board
│   ├── Player
│   ├── Knight
│   ├── Tile
│   └── Move
│
├── ai/
│   ├── Minimax
│   ├── Heuristic
│   └── TreeNode
│
├── ui/
│   ├── MainWindow
│   ├── BoardView
│   ├── HUD
│   └── Assets
│
├── controller/
│   └── GameController
│
└── main
```

------------------------------------------------------------------------

# Flujo de Trabajo

``` text
Día 1
├── Perea → Lógica del juego
├── Manuel → Interfaz
└── Allan → IA

        ↓

Día 2
├── Manuel conecta la GUI
├── Allan conecta Minimax
└── Perea apoya integración

        ↓

Día 3
├── Pruebas
├── Corrección de errores
└── Informe final
```

Este plan permite que los tres desarrolladores trabajen en paralelo
durante la mayor parte del proyecto, reduciendo conflictos de
integración y facilitando el uso de Git mediante una separación clara
por módulos.
