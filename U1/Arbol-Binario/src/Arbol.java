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
 * Árbol binario de búsqueda cuyos nodos se ordenan por nombre.
 * Para cada nodo, los nombres de su subárbol izquierdo son menores que el suyo
 * y los de su subárbol derecho son mayores
 */
public class Arbol {
    private Nodo raiz; // Punto de entrada al árbol. Vale null cuando el árbol está vacío

    public Arbol() {
        this.raiz = null;
    }

    public boolean vacio() {
        return raiz == null;
    }

    // Devuelve el nodo que contiene el nombre indicado, o null si no se encuentra en el árbol
    public Nodo buscarNodo(String nombre) {
        return buscar(raiz, nombre);
    }

    /*
     * Búsqueda recursiva propia del árbol binario de búsqueda.
     * En cada paso compara el nombre con el del nodo actual y continúa únicamente
     * por el subárbol donde podría encontrarse, descartando el otro por completo
     */
    private Nodo buscar(Nodo actual, String nombre) {
        if (actual == null) {
            return null;
        }
        // compareTo compara los nombres según el orden de sus caracteres, por eso distingue mayúsculas de minúsculas.
        // Devuelve un valor negativo si el nombre precede al del nodo, cero si son iguales y positivo si lo sucede
        int comparacion = nombre.compareTo(actual.getNombre());
        if (comparacion == 0) {
            return actual;
        }
        if (comparacion < 0) {
            return buscar(actual.getIzquierdo(), nombre);
        }
        return buscar(actual.getDerecho(), nombre);
    }

    public void insertar(String nombre) {
        raiz = insertar(raiz, nombre);
    }

    /*
     * Desciende recursivamente hasta encontrar una posición vacía y ahí crea el nodo nuevo.
     * Devuelve el nodo actual para que su padre conserve la referencia a él al regresar de la recursión
     */
    private Nodo insertar(Nodo actual, String nombre) {
        if (actual == null) {
            return new Nodo(nombre);
        }
        int comparacion = nombre.compareTo(actual.getNombre());
        if (comparacion < 0) {
            actual.setIzquierdo(insertar(actual.getIzquierdo(), nombre));
        } else if (comparacion > 0) {
            actual.setDerecho(insertar(actual.getDerecho(), nombre));
        }
        // Un nombre repetido no se inserta, por lo que el árbol permanece igual
        return actual;
    }

    public Nodo getRaiz() {
        return raiz;
    }
}
