/*
 * Inteligencia Artificial
 * Unidad 1 - Árbol binario de búsqueda
 * Horario: 6:00 - 7:00 p.m.
 *
 * Alumna: Crespo Hernández Kitzia Marisol
 * No. de control: C23171148
 *
 * Actividad diagnóstica
 */

/*
 * Programa principal de la actividad diagnóstica.
 * Construye un árbol binario de búsqueda con varios nombres y comprueba el funcionamiento de vacio() y buscarNodo()
 */
public class App {
    public static void main(String[] args) {
        Arbol arbol = new Arbol();

        System.out.println("Árbol recién creado");
        System.out.println("¿Está vacío? " + arbol.vacio());

        // El primer nombre se convierte en la raíz y cada uno de los siguientes se ubica según el orden del árbol
        String[] nombres = { "Kitzia", "Hannia", "Sofia", "Mario", "Raul", "Ximena" };
        for (String nombre : nombres) {
            arbol.insertar(nombre);
        }

        System.out.println();
        System.out.println("Después de insertar " + nombres.length + " nombres");
        System.out.println("¿Está vacío? " + arbol.vacio());
        System.out.println("Nodo raíz: " + arbol.getRaiz().getNombre());

        // Si el árbol está bien construido, el recorrido en orden muestra los nombres de menor a mayor
        System.out.print("Recorrido en orden: ");
        enOrden(arbol.getRaiz());
        System.out.println();

        // Casos de prueba con un nodo interno, una hoja y un nombre que no existe en el árbol
        System.out.println();
        System.out.println("Pruebas de buscarNodo");
        buscar(arbol, "Kitzia");
        buscar(arbol, "Ximena");
        buscar(arbol, "Lucia");
    }

    private static void buscar(Arbol arbol, String nombre) {
        Nodo encontrado = arbol.buscarNodo(nombre);
        if (encontrado == null) {
            System.out.println("  " + nombre + " no está en el árbol");
        } else {
            System.out.println("  " + nombre + " encontrado, hijos: izquierdo "
                    + textoHijo(encontrado.getIzquierdo()) + ", derecho "
                    + textoHijo(encontrado.getDerecho()));
        }
    }

    // Entrega el nombre del hijo, o un guion cuando ese hijo no existe
    private static String textoHijo(Nodo hijo) {
        if (hijo == null) {
            return "-";
        }
        return hijo.getNombre();
    }

    /*
     * Recorrido en orden. Visita el subárbol izquierdo, después el nodo actual y al final
     * el subárbol derecho, de modo que los nombres aparecen de menor a mayor
     */
    private static void enOrden(Nodo actual) {
        if (actual == null) {
            return;
        }
        enOrden(actual.getIzquierdo());
        System.out.print(actual.getNombre() + " ");
        enOrden(actual.getDerecho());
    }
}
