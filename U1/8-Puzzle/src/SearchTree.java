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

import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Set;
import java.util.Stack;

/*
 * Árbol de búsqueda del 8-puzzle.
 * Contiene las búsquedas no informadas vistas en clase (primero en anchura,
 * primero en profundidad y costo uniforme). Todas parten del mismo nodo raíz.
 */
public class SearchTree {
    Node root;
    String goalState;
    String initialState;

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
                break;
            }
            // Genera los sucesores del estado actual y encola los que no han sido visitados.
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    queue.add(child);
            }
        }
        // Nodos procesados, estados visitados y tamaño final de la cola.
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Queue: " + queue.size());
        System.out.println();
    }

    // Búsqueda primero en profundidad (DFS).
    // Sigue una rama hasta el fondo antes de probar otra.
    // Mismo procedimiento que BFS, pero con una pila (LIFO) en lugar de una cola.
    public void depthFirstSearch() {
        System.out.println("--- Depth First Search ---");
        int time = 0;
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
                break;
            }
            // Apila los sucesores no visitados. El último apilado será el siguiente en procesarse.
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState()))
                    stack.push(child);
            }
        }
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Stack: " + stack.size());
        System.out.println();
    }

    // Búsqueda de costo uniforme (UCS).
    // Expande primero el nodo con menor costo acumulado usando una cola de prioridad.
    // Como cada movimiento cuesta 1, se comporta igual que BFS.
    public void uniformCostSearch() {
        System.out.println("*** Uniform Cost Search ***");
        int time = 0;
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
        }
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Priority Queue: " + queue.size());
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
