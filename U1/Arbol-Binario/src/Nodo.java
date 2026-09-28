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
 * Nodo del árbol binario de búsqueda.
 * Almacena un nombre y las referencias a sus dos hijos. Un nodo sin hijos se denomina hoja
 */
public class Nodo {
    private String nombre; // Clave que determina la posición del nodo dentro del árbol
    private Nodo izquierdo; // Raíz del subárbol con los nombres menores que este
    private Nodo derecho; // Raíz del subárbol con los nombres mayores que este

    public Nodo(String nombre) {
        this.nombre = nombre;
        this.izquierdo = null;
        this.derecho = null;
    }

    public String getNombre() {
        return nombre;
    }

    public Nodo getIzquierdo() {
        return izquierdo;
    }

    public void setIzquierdo(Nodo izquierdo) {
        this.izquierdo = izquierdo;
    }

    public Nodo getDerecho() {
        return derecho;
    }

    public void setDerecho(Nodo derecho) {
        this.derecho = derecho;
    }
}
