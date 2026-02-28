# La Intuición: Más de un cocinero en la cocina

Imagina que un algoritmo secuencial es una receta de cocina que una sola persona sigue paso a paso. Es predecible: si la receta dice "agrega sal y luego bate", siempre ocurrirá en ese orden.

Un ****algoritmo concurrente**** es lo que pasa cuando metes a 3 cocineros en la misma cocina pequeña para preparar la misma cena, compartiendo un solo salero y una sola estufa.

## El gran problema: El entrelazamiento (Interleaving)

En concurrencia, no sabemos en qué orden exacto se ejecutarán las instrucciones de los diferentes hilos. El sistema operativo puede pausar a un hilo en cualquier momento.

Si el Hilo A y el Hilo B quieren hacer `x = x + 1`, podríamos tener este desastre:

1.  Hilo A lee que x es 0.
2.  *Pausa del sistema*
3.  Hilo B lee que x es 0.
4.  Hilo B suma 1 y escribe x=1.
5.  Hilo A (que se quedó con el 0 original) suma 1 y escribe x=1.
6.  **¡Perdimos un incremento!** El resultado debió ser 2.

# Definición Formal

Un algoritmo concurrente es un conjunto de instrucciones diseñadas para ser ejecutadas por múltiples hilos de control que interactúan a través de ****memoria compartida**** o paso de mensajes.

# ¿Cómo sabemos si el algoritmo "está bien"?

A diferencia de los algoritmos secuenciales, aquí no basta con que el resultado sea correcto. Necesitamos dos dimensiones de análisis:

## 1. Seguridad (Safety): "Nada malo va a pasar"

Aquí es donde entran nuestras nociones de corrección:

- ****Linealizabilidad:**** ¿Parece que las cosas ocurren de forma atómica e instantánea?
- ****Consistencia Secuencial:**** ¿Se respeta al menos el orden de cada hilo?

## 2. Viveza (Liveness): "Algo bueno va a pasar eventualmente"

- ****Wait-free:**** Ningún hilo se queda esperando a otro.
- ****Deadlock-free:**** El sistema no se queda "trabado" para siempre.

# Ejemplo: El Contador "Simple"

Este es el ejemplo clásico que puedes correr en tu computadora para ver cómo falla la concurrencia:

``` java
public class Contador {
    private int valor = 0;

    public void inc() {
        valor++; // ¡Esta linea no es atomica!
    }

    public int get() {
        return valor;
    }
}
```

Para arreglar esto y hacerlo ****Linealizable****, necesitaríamos usar un `lock` o, como veremos más adelante, convertir esa variable en `volatile` o usar un `AtomicInteger`.

# Conexión con el siguiente tema: El Consenso

Si los algoritmos concurrentes son tan difíciles de coordinar, ¿cómo logran los hilos ponerse de acuerdo en algo? Ese es el problema del ****Consenso****, y descubriremos que hay objetos "más poderosos" que otros para lograrlo.
