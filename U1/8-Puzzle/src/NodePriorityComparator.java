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

import java.util.Comparator;

/*
 * Comparator utilizado por la PriorityQueue de la búsqueda de costo uniforme.
 * Ordena los nodos por costo acumulado, de menor a mayor, de modo que
 * la cola de prioridad siempre entregue primero el nodo más barato.
 */
public class NodePriorityComparator implements Comparator<Node> {

    @Override
    public int compare(Node n1, Node n2) {
        return Integer.compare(n1.getCost(), n2.getCost());
    }
}
