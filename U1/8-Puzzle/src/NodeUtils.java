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

import java.util.ArrayList;
import java.util.List;

/*
 * Utilerías del 8-puzzle. Aquí viven la función sucesor y el formato del tablero.
 */
public class NodeUtils {

    // Intercambia dos casillas. Como String es inmutable, se hace sobre un arreglo de caracteres.
    private static String swapPositions(String state, int pos1, int pos2) {
        char[] arr = state.toCharArray();
        char temp = arr[pos1];
        arr[pos1] = arr[pos2];
        arr[pos2] = temp;
        return new String(arr);
    }

    // Función sucesor. Genera todos los estados que se obtienen al mover
    // el espacio vacío a una casilla adyacente.
    public static List<Node> generateChildren(Node parentNode) {

        /*
         * Ejemplo con el espacio vacío en la posición 6:
         *
         *  1 2 3        1 2 3      1 2 3
         *  4 5 6   =>     5 6  +   4 5 6
         *    7 8        4 7 8      7   8
         *
         * "123456 78" => ["123 56478", "1234567 8"]
         */

        List<Node> successors = new ArrayList<>();
        int zeroPos = parentNode.getState().indexOf(" ");

        /*
         * Posiciones del tablero:
         *
         * 0 1 2
         * 3 4 5
         * 6 7 8
         *
         * Para cada posición del espacio vacío se indican
         * las posiciones con las que puede intercambiarse.
         */
        int[][] adjacentPositions = {
            {1, 3},           // posición 0
            {0, 2, 4},        // posición 1
            {1, 5},           // posición 2
            {0, 4, 6},        // posición 3
            {1, 3, 5, 7},     // posición 4
            {2, 4, 8},        // posición 5
            {3, 7},           // posición 6
            {4, 6, 8},        // posición 7
            {5, 7}            // posición 8
        };

        // Cada hijo se crea con referencia a su nodo padre. Esa trazabilidad
        // es la que permite reconstruir la ruta de solución.
        for (int adjPos : adjacentPositions[zeroPos]) {
            String newState = swapPositions(parentNode.getState(), zeroPos, adjPos);
            successors.add(new Node(newState, parentNode));
        }

        return successors;
    }

    // Convierte la cadena de 9 caracteres en un tablero de 3 x 3 para imprimirlo.
    public static String formatState(String state){
        String formattedState = "";
        for(int i = 0; i < state.length(); i++){
            formattedState += state.charAt(i) + " ";
            if((i + 1) % 3 == 0){
                formattedState += "\n";
            }
        }
        return formattedState;
    }
}
