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

import java.util.Comparator;

/*
 * Comparator utilizado por la PriorityQueue de la búsqueda A*.
 * Ordena los nodos por f(n), de menor a mayor, de modo que la cola de prioridad
 * entregue primero el nodo con el menor costo estimado total. En las búsquedas
 * no informadas el orden dependía únicamente del costo acumulado.
 */
public class NodePriorityComparator implements Comparator<Node> {

    @Override
    public int compare(Node n1, Node n2) {
        return Integer.compare(n1.getF(), n2.getF());
    }
}
