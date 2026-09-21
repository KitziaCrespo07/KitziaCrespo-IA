/*
 * Inteligencia Artificial
 * Unidad 1 - Algoritmos de búsqueda aplicados al 8-puzzle
 * Horario: 6:00 - 7:00 p.m.
 *
 * Alumna: Crespo Hernández Kitzia Marisol
 * No. de control: C23171148
 *
 * 8-puzzle
 */

import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;
import java.util.Stack;

/*
 * Árbol de búsqueda del 8-puzzle.
 * Contiene las búsquedas no informadas del primer parcial (primero en anchura,
 * primero en profundidad, costo uniforme, profundidad limitada y profundidad
 * iterativa) y la búsqueda bidireccional, que es opcional. Todas parten del mismo nodo raíz.
 */
public class SearchTree {
    Node root;
    String goalState;
    String initialState;

    // Contadores de la búsqueda en profundidad limitada. Son atributos de la clase
    // porque el método recursivo los va actualizando en cada llamada.
    int time;
    int maxDepth;

    public SearchTree(String initialState, String goalState) {
        this.initialState = initialState;
        this.goalState = goalState;
        // El nodo raíz corresponde al estado inicial y no tiene padre.
        this.root = new Node(initialState, null);
    }

    // Búsqueda primero en anchura (BFS).
    // Explora el árbol por niveles usando una cola FIFO.
    public void breadthFirstSearch() {
        System.out.println("===== Breadth First Search =====");
        // Cuenta los nodos procesados durante esta ejecución.
        int time = 0;
        // Registra el mayor número de nodos que llegó a tener la cola.
        int maxQueue = 0;
        long startTime = System.nanoTime();
        // Estados visitados, para no volver a procesar un tablero ya explorado.
        Set<String> visited = new HashSet<String>();
        Node currentNode = root;
        Queue<Node> queue = new LinkedList<>();
        queue.add(currentNode);
        // Continúa la búsqueda mientras existan nodos pendientes por explorar.
        while (!queue.isEmpty()) {
            time++;
            // Extrae el nodo más antiguo de la cola (FIFO) y lo marca como visitado.
            currentNode = queue.poll();
            visited.add(currentNode.getState());
            //System.out.println(NodeUtils.formatState(currentNode.getState()));
            // Test objetivo. Si el estado actual es el objetivo, se imprime la ruta y termina.
            if(currentNode.getState().equals(goalState)) {
                System.out.println("Goal state found: " + currentNode.getState());
                printPath(currentNode);
                System.out.println("Profundidad de la solucion: " + currentNode.getDepth());
                break;
            }
            // Genera los sucesores del estado actual y encola los que no han sido visitados.
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    queue.add(child);
            }
            if (queue.size() > maxQueue)
                maxQueue = queue.size();
        }
        long endTime = System.nanoTime();
        // Nodos procesados, estados visitados, tamaño final y máximo de la cola, y tiempo real.
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Queue: " + queue.size());
        System.out.println("Max Queue: " + maxQueue);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Búsqueda primero en profundidad (DFS).
    // Sigue una rama hasta el fondo antes de probar otra.
    // Mismo procedimiento que BFS, pero con una pila (LIFO) en lugar de una cola.
    public void depthFirstSearch() {
        System.out.println("--- Depth First Search ---");
        int time = 0;
        int maxStack = 0;
        long startTime = System.nanoTime();
        Set<String> visited = new HashSet<String>();
        Node currentNode = root;
        Stack<Node> stack = new Stack<>();
        stack.push(currentNode);
        while (!stack.isEmpty()) {
            time++;
            // Extrae el último nodo agregado a la pila (LIFO) y lo marca como visitado.
            currentNode = stack.pop();
            visited.add(currentNode.getState());
            // Test objetivo.
            if(currentNode.getState().equals(goalState)) {
                System.out.println("Goal state found: " + currentNode.getState());
                printPath(currentNode);
                System.out.println("Profundidad de la solucion: " + currentNode.getDepth());
                break;
            }
            // Apila los sucesores no visitados. El último apilado será el siguiente en procesarse.
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    stack.push(child);
            }
            if (stack.size() > maxStack)
                maxStack = stack.size();
        }
        long endTime = System.nanoTime();
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Stack: " + stack.size());
        System.out.println("Max Stack: " + maxStack);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Búsqueda de costo uniforme (UCS).
    // Expande primero el nodo con menor costo acumulado usando una cola de prioridad.
    // Como cada movimiento cuesta 1, se comporta igual que BFS.
    public void uniformCostSearch() {
        System.out.println("*** Uniform Cost Search ***");
        int time = 0;
        int maxQueue = 0;
        long startTime = System.nanoTime();
        Set<String> visited = new HashSet<String>();
        // El nodo raíz entra con costo 0.
        Node currentNode = root;
        PriorityQueue<Node> queue = new PriorityQueue<>(new NodePriorityComparator());
        queue.add(currentNode);
        while (!queue.isEmpty()) {
            time++;
            // Extrae el nodo de menor costo acumulado y lo marca como visitado.
            currentNode = queue.poll();
            visited.add(currentNode.getState());
            // Test objetivo.
            if(currentNode.getState().equals(goalState)) {
                System.out.println("Goal state found: " + currentNode.getState());
                printPath(currentNode);
                System.out.println("Profundidad de la solucion: " + currentNode.getDepth());
                System.out.println("Costo de la solucion: " + currentNode.getCost());
                break;
            }
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState())) {
                    // Cada movimiento cuesta 1, así que el hijo hereda el costo del padre más 1.
                    child.setCost(child.getParent().getCost() + 1);
                    queue.add(child);
                }
            }
            if (queue.size() > maxQueue)
                maxQueue = queue.size();
        }
        long endTime = System.nanoTime();
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Priority Queue: " + queue.size());
        System.out.println("Max Priority Queue: " + maxQueue);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Búsqueda en profundidad limitada.
    // Funciona como DFS, pero detiene la expansión al alcanzar el límite establecido.
    // Se implementa de forma recursiva, como el pseudocódigo del libro.
    public void depthLimitedSearch(int limit) {
        System.out.println("--- Depth Limited Search (limite " + limit + ") ---");
        time = 0;
        maxDepth = 0;
        // Aquí visited guarda solo los estados del camino actual (de la raíz al nodo actual).
        // Con eso basta para no dar vueltas en ciclos sin bloquear otras ramas.
        Set<String> visited = new HashSet<String>();
        long startTime = System.nanoTime();
        Node result = recursiveDLS(root, limit, visited);
        long endTime = System.nanoTime();
        if (result != null) {
            System.out.println("Goal state found: " + result.getState());
            printPath(result);
            System.out.println("Profundidad de la solucion: " + result.getDepth());
        } else {
            System.out.println("No se encontro la solucion con limite " + limit);
        }
        // La memoria que ocupa es el camino actual, de a lo más maxDepth + 1 nodos.
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Profundidad maxima alcanzada: " + maxDepth);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Recorre el árbol en profundidad de forma recursiva.
    // Regresa el nodo objetivo si lo encuentra dentro del límite, o null si no.
    private Node recursiveDLS(Node currentNode, int limit, Set<String> visited) {
        time++;
        if (currentNode.getDepth() > maxDepth)
            maxDepth = currentNode.getDepth();
        // Test objetivo.
        if (currentNode.getState().equals(goalState))
            return currentNode;
        // Al llegar al límite la rama se corta y ya no se generan sucesores.
        if (currentNode.getDepth() >= limit)
            return null;
        // El estado actual pasa a formar parte del camino que se está explorando.
        visited.add(currentNode.getState());
        List<Node> children = NodeUtils.generateChildren(currentNode);
        for (Node child : children) {
            if (!visited.contains(child.getState())) {
                Node result = recursiveDLS(child, limit, visited);
                if (result != null)
                    return result;
            }
        }
        // Al regresar de la rama, el estado deja de formar parte del camino actual.
        visited.remove(currentNode.getState());
        return null;
    }

    // Búsqueda en profundidad iterativa.
    // Repite la búsqueda limitada aumentando el límite de uno en uno hasta encontrar la meta.
    public void iterativeDeepeningSearch() {
        System.out.println("===== Iterative Deepening Search =====");
        // Suma los nodos procesados de todas las iteraciones.
        int totalTime = 0;
        Node result = null;
        long startTime = System.nanoTime();
        // Ninguna solución del 8-puzzle necesita más de 31 movimientos.
        for (int limit = 0; limit <= 31; limit++) {
            time = 0;
            maxDepth = 0;
            Set<String> visited = new HashSet<String>();
            result = recursiveDLS(root, limit, visited);
            totalTime += time;
            System.out.println("Limite " + limit + " - Time: " + time);
            if (result != null)
                break;
        }
        long endTime = System.nanoTime();
        if (result != null) {
            System.out.println("Goal state found: " + result.getState());
            printPath(result);
            System.out.println("Profundidad de la solucion: " + result.getDepth());
        } else {
            System.out.println("No se encontro la solucion");
        }
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time (todas las iteraciones): " + totalTime);
        System.out.println("Profundidad maxima alcanzada: " + maxDepth);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Búsqueda bidireccional (opcional).
    // Corre dos búsquedas en anchura a la vez, una desde el estado inicial y otra desde
    // el estado objetivo, y termina cuando las dos llegan a un mismo estado.
    // En el 8-puzzle los movimientos son reversibles, por eso ambas usan la misma función sucesor.
    public void bidirectionalSearch() {
        System.out.println("===== Bidirectional Search (opcional) =====");
        int time = 0;
        int maxQueue = 0;
        long startTime = System.nanoTime();
        // Aquí se guarda el nodo y no solo el estado, para poder unir las dos rutas cuando se encuentren.
        Map<String, Node> visitedStart = new HashMap<String, Node>();
        Map<String, Node> visitedGoal = new HashMap<String, Node>();
        Queue<Node> queueStart = new LinkedList<>();
        Queue<Node> queueGoal = new LinkedList<>();
        // La búsqueda hacia atrás tiene su propia raíz, que es el estado objetivo.
        Node goalRoot = new Node(goalState, null);
        queueStart.add(root);
        visitedStart.put(root.getState(), root);
        queueGoal.add(goalRoot);
        visitedGoal.put(goalRoot.getState(), goalRoot);
        // Nodo de cada lado en el que se encontraron las dos búsquedas.
        Node meetStart = null;
        Node meetGoal = null;
        // Si el estado inicial ya es el objetivo, las dos búsquedas coinciden desde la raíz.
        if (initialState.equals(goalState)) {
            meetStart = root;
            meetGoal = goalRoot;
        }
        while (meetStart == null && !queueStart.isEmpty() && !queueGoal.isEmpty()) {
            // Un nivel completo desde el estado inicial.
            int levelSize = queueStart.size();
            for (int i = 0; i < levelSize && meetStart == null; i++) {
                time++;
                Node currentNode = queueStart.poll();
                List<Node> children = NodeUtils.generateChildren(currentNode);
                for (Node child : children) {
                    // Si la otra búsqueda ya pasó por este estado, las dos rutas se tocan.
                    if (visitedGoal.containsKey(child.getState())) {
                        meetStart = child;
                        meetGoal = visitedGoal.get(child.getState());
                        break;
                    }
                    if (!visitedStart.containsKey(child.getState())) {
                        visitedStart.put(child.getState(), child);
                        queueStart.add(child);
                    }
                }
            }
            if (meetStart != null)
                break;
            // Un nivel completo desde el estado objetivo, con la misma lógica.
            levelSize = queueGoal.size();
            for (int i = 0; i < levelSize && meetGoal == null; i++) {
                time++;
                Node currentNode = queueGoal.poll();
                List<Node> children = NodeUtils.generateChildren(currentNode);
                for (Node child : children) {
                    if (visitedStart.containsKey(child.getState())) {
                        meetGoal = child;
                        meetStart = visitedStart.get(child.getState());
                        break;
                    }
                    if (!visitedGoal.containsKey(child.getState())) {
                        visitedGoal.put(child.getState(), child);
                        queueGoal.add(child);
                    }
                }
            }
            if (queueStart.size() + queueGoal.size() > maxQueue)
                maxQueue = queueStart.size() + queueGoal.size();
        }
        long endTime = System.nanoTime();
        if (meetStart != null) {
            System.out.println("Goal state found: " + goalState);
            System.out.println("Estado de encuentro: " + meetStart.getState());
            // Del estado inicial al encuentro se imprime con los padres del lado inicial.
            printPath(meetStart);
            // Del encuentro al objetivo se sube por los padres del lado objetivo,
            // porque en ese árbol el padre siempre está un paso más cerca de la meta.
            Node node = meetGoal.getParent();
            while (node != null) {
                System.out.println(NodeUtils.formatState(node.getState()));
                node = node.getParent();
            }
            System.out.println("Profundidad de la solucion: " + (meetStart.getDepth() + meetGoal.getDepth()));
        } else {
            System.out.println("No se encontro la solucion");
        }
        // Los estados visitados y las colas se suman porque son dos búsquedas.
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + (visitedStart.size() + visitedGoal.size()));
        System.out.println("Queue (ambas): " + (queueStart.size() + queueGoal.size()));
        System.out.println("Max Queue (ambas): " + maxQueue);
        System.out.println("Tiempo real (ms): " + (endTime - startTime) / 1000000.0);
        System.out.println();
    }

    // Recorre primero los nodos padre para imprimir la solución
    // desde el estado inicial hasta el estado objetivo, y no al revés.
    public void printPath(Node node) {
        if (node == null) {
            return;
        }
        printPath(node.getParent());
        System.out.println(NodeUtils.formatState(node.getState()));
    }
}
