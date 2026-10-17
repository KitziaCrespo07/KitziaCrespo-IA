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
 * Programa principal. Función heurística aplicada al 8-puzzle.
 *
 * Muestra la estimación de dos funciones heurísticas sobre el estado inicial
 * y resuelve el 8-puzzle mediante el algoritmo A* con cada una de ellas,
 * para comparar la cantidad de nodos procesados.
 */
public class App {
    public static void main(String[] args) throws Exception {

        // El tablero se representa como una cadena de 9 caracteres.
        // El espacio en blanco representa la casilla vacía.
        String initialState = "7621 3458"; // Estado inicial del puzzle
        String goalState = "12345678 "; // Estado objetivo del puzzle

        System.out.println("Initial State:");
        System.out.println(NodeUtils.formatState(initialState));
        System.out.println("Goal State:");
        System.out.println(NodeUtils.formatState(goalState));

        // Calcula y muestra las estimaciones heurísticas del estado inicial
        System.out.println("--- Funcion heuristica sobre el estado inicial ---");
        System.out.println("Fichas fuera de lugar: "
                + Heuristica.fichasFueraDeLugar(initialState, goalState));
        System.out.println("Distancia Manhattan: "
                + Heuristica.distanciaManhattan(initialState, goalState));
        System.out.println();

        // Ejecuta A* con cada heurística de forma independiente.
        SearchTree primeraBusqueda = new SearchTree(initialState, goalState);
        primeraBusqueda.aStarSearch(Heuristica.FICHAS_FUERA_DE_LUGAR);

        SearchTree segundaBusqueda = new SearchTree(initialState, goalState);
        segundaBusqueda.aStarSearch(Heuristica.DISTANCIA_MANHATTAN);

        System.out.println("End");
    }
}
