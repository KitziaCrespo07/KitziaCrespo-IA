/*
 * Inteligencia Artificial
 * Unidad 1 - Función heurística aplicada al 8-puzzle
 * Horario: 6:00 - 7:00 p.m.
 *
 * Alumna: Crespo Hernández Kitzia Marisol
 * No. de control: C23171148
 *
 * 8-puzzle con búsqueda informada
 */

import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Set;

/*
 * Árbol de búsqueda del 8-puzzle mediante el algoritmo A*.
 *
 * Utiliza una cola de prioridad ordenada por f(n) = g(n) + h(n),
 * considerando el costo acumulado y la estimación heurística
 * para orientar la búsqueda hacia el estado objetivo.
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

    // Ejecuta A* utilizando fichas fuera de lugar o distancia Manhattan.
    // El algoritmo es el mismo, únicamente cambia la heurística utilizada.
    public void aStarSearch(int heuristica) {
        System.out.println("*** A* Search con " + Heuristica.nombre(heuristica) + " ***");
        int time = 0;
        int maxQueue = 0;
        int repetidos = 0;
        Set<String> visited = new HashSet<String>();
        Node currentNode = root;
        Node result = null;
        PriorityQueue<Node> queue = new PriorityQueue<>(new NodePriorityComparator());
        // El nodo raíz entra con costo acumulado 0 y con su propia estimación.
        root.setCost(0);
        root.setHeuristic(Heuristica.calcular(heuristica, root.getState(), goalState));
        queue.add(root);
        maxQueue = queue.size();
        long startTime = System.nanoTime();
        while (!queue.isEmpty()) {
            // Cuenta los nodos extraídos de la cola, incluidos los repetidos
            time++;
            // Extrae el nodo con la f(n) más baja.
            currentNode = queue.poll();
            // Un mismo estado puede llegar a la cola por varios caminos. Si ya se
            // expandió antes, se descarta en lugar de volver a generar sus sucesores.
            if (!visited.add(currentNode.getState())) {
                repetidos++;
                continue;
            }
            // Test objetivo, se comprueba si se alcanzó el estado objetivo
            if (currentNode.getState().equals(goalState)) {
                result = currentNode;
                break;
            }
            List<Node> children = NodeUtils.generateChildren(currentNode);
            for (Node child : children) {
                if (!visited.contains(child.getState())) {
                    // Cada movimiento cuesta 1, así que el hijo hereda el costo del padre más 1.
                    child.setCost(child.getParent().getCost() + 1);
                    // A cada hijo se le calcula la heurística antes de entrar a la cola.
                    child.setHeuristic(Heuristica.calcular(heuristica, child.getState(), goalState));
                    queue.add(child);
                }
            }
            if (queue.size() > maxQueue) {
                maxQueue = queue.size();
            }
        }
        // El cronómetro se detiene aquí, antes de imprimir, para medir solo la búsqueda. 
        long endTime = System.nanoTime();
        if (result != null) {
            System.out.println("Goal state found: " + result.getState());
            printPath(result);
            System.out.println("Profundidad de la solucion: " + result.getDepth());
            System.out.println("Costo de la solucion: " + result.getCost());
        } else {
            System.out.println("No se encontro la solucion");
        }
        System.out.println("--- Datos estadisticos ---");
        System.out.println("Heuristica del estado inicial: "
                + Heuristica.calcular(heuristica, initialState, goalState));
        System.out.println("Time: " + time);
        System.out.println("Estados visitados: " + visited.size());
        System.out.println("Nodos repetidos descartados: " + repetidos);
        System.out.println("Priority Queue: " + queue.size());
        System.out.println("Max Priority Queue: " + maxQueue);
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
