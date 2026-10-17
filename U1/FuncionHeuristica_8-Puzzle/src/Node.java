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

/*
 * Nodo del árbol de búsqueda.
 * Representa un estado del 8-puzzle junto con la información necesaria
 * para recorrer el árbol y reconstruir la ruta de solución. Respecto al de las
 * búsquedas no informadas, incorpora además la estimación heurística del estado.
 */
public class Node {
    // Tablero como cadena de 9 caracteres. El espacio en blanco es la casilla vacía.
    private String state;
    // Nodo padre. Permite regresar desde el estado objetivo hasta el estado inicial.
    private Node parent;
    // Nivel del nodo dentro del árbol de búsqueda.
    private int depth;
    // Costo real acumulado desde el nodo raíz. Corresponde a g(n).
    private int cost;
    // Costo estimado de este nodo al estado objetivo. Corresponde a h(n).
    private int heuristic;

    public Node(String state, Node parent) {
        this.state = state;
        this.parent = parent;
        // El nodo raíz tiene profundidad 0 y cada hijo queda un nivel por debajo de su padre.
        if (parent != null) {
            this.depth = parent.getDepth() + 1;
        }
    }

    // Valor con el que A* ordena la cola de prioridad.
    // f(n) = g(n) + h(n), el costo real acumulado más el costo estimado que resta.
    public int getF() {
        return cost + heuristic;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public int getDepth() {
        return depth;
    }

    public void setDepth(int depth) {
        this.depth = depth;
    }

    public int getCost() {
        return cost;
    }

    public void setCost(int cost) {
        this.cost = cost;
    }

    public int getHeuristic() {
        return heuristic;
    }

    public void setHeuristic(int heuristic) {
        this.heuristic = heuristic;
    }
}
