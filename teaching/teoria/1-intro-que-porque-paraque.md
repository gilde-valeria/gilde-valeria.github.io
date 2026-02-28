# 1. ¿Qué es la Concurrencia?

Coordinar agentes en presencia de adversarios.

> "Un programa concurrente consiste en una colección de agentes que cooperan o compiten por recursos compartidos."

El reto del programador no es escribir el código, sino razonar sobre todas las posibles **historias de ejecución** (interleavings) que se pueden generar.



# 2. Un Poco de Historia: De la Necesidad a la Disciplina

## El Origen (1961 - Atlas Computer)
La concurrencia nació bajo el nombre de **Multiprogramming**. Inicialmente, "Distribuido" y "Concurrente" eran lo mismo.

- **Objetivo original:** No era ir más rápido, sino **no desperdiciar el CPU**. Mientras un proceso esperaba I/O, el CPU saltaba a otro.



## La Evolución Forzada (El fin de la fiesta del silicio)
Chocamos contra tres muros físicos:
1. **Power Wall:** Calor excesivo.
2. **Memory Wall:** CPU vs RAM speed gap.
3. **ILP Wall:** Límites del paralelismo de instrucciones.

**La solución:** Procesadores **multi-core**. La complejidad pasó del hardware al software.



# 3. La Gran Unificación (Raynal & Rajsbaum)
**Dos caras de la misma moneda.**

- **Cómputo Paralelo:** Busca **Eficiencia**. Entorno "amigable".
- **Cómputo Distribuido:** Busca **Coordinación**. Entorno "hostil" (fallos y asincronía).



# 4. Nuestro Modelo de Estudio
- **Agentes:** Hilos (**threads**).
- **Comunicación:** **Memoria Compartida** mediante **Objetos Compartidos**.
- **Adversario:** Un scheduler asíncrono.

![Arquitectura de procesador](../../images/procesador_atomic.png)

---

### Siguiente paso en el Roadmap:
- [Historias y el modelo de interleaving de Raynal](nota.html?src=teoria/2-historias-con-moraleja.md)
- [Linealizabilidad: ¿Cómo probar la corrección?](nota.html?src=teoria/3-linearizabilidad-vs-sc.md)