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

/*
 * Avance del 8-puzzle con las búsquedas no informadas vistas en clase.
 *
 * Programa principal. Ejecuta las tres búsquedas sobre el mismo estado inicial
 * y el mismo estado objetivo, para que sus datos estadísticos sean comparables.
 */
public class App {
    public static void main(String[] args) throws Exception {

        // El tablero se representa como una cadena de 9 caracteres, leída por renglones.
        // El espacio en blanco es la casilla vacía.
        String initialState = "7621 3458"; // Estado inicial del puzzle
        String goalState = "12345678 "; // Estado objetivo del puzzle

        System.out.println("Initial State:");
        System.out.println(NodeUtils.formatState(initialState));
        System.out.println("Goal State:");
        System.out.println(NodeUtils.formatState(goalState));

        SearchTree searchTree = new SearchTree(initialState, goalState);

        searchTree.breadthFirstSearch();
        searchTree.uniformCostSearch();
        searchTree.depthFirstSearch();

        System.out.println("End");
    }
}
