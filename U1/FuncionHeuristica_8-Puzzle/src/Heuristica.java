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
 * Funciones heurísticas del 8-puzzle.
 *
 * Estiman cuántos movimientos faltan para alcanzar el estado objetivo.
 * Ambas excluyen el espacio vacío y no sobreestiman los movimientos necesarios.
 */

public class Heuristica {

    // Identificadores para seleccionar la heurística que utilizará A*.
    public static final int FICHAS_FUERA_DE_LUGAR = 1;
    public static final int DISTANCIA_MANHATTAN = 2;

    // Heurística 1. Cuenta las fichas que no están en su posición objetivo.
    // Su estimación no supera los movimientos necesarios, ya que cada ficha
    // fuera de lugar necesita al menos un movimiento para llegar a su posición.
    public static int fichasFueraDeLugar(String estado, String objetivo) {
        int fuera = 0;
        for (int i = 0; i < estado.length(); i++) {
            // El espacio vacío no representa una ficha, por lo que se excluye del cálculo.
            if (estado.charAt(i) == ' ') {
                continue;
            }
            if (estado.charAt(i) != objetivo.charAt(i)) {
                fuera++;
            }
        }
        return fuera;
    }

    // Heurística 2. Suma, para cada ficha, los renglones y columnas que la separan de
    // su casilla objetivo. Resulta más informada que la heurística 1, ya que una ficha
    // fuera de lugar puede requerir varios movimientos y no solo uno.
    public static int distanciaManhattan(String estado, String objetivo) {
        int distancia = 0;
        for (int i = 0; i < estado.length(); i++) {
            char ficha = estado.charAt(i);
            if (ficha == ' ') {
                continue;
            }
            int destino = objetivo.indexOf(ficha);
            // El renglón de una casilla es su posición entre 3 y la columna es el residuo.
            int renglones = Math.abs(i / 3 - destino / 3);
            int columnas = Math.abs(i % 3 - destino % 3);
            distancia += renglones + columnas;
        }
        return distancia;
    }

    // Calcula la heurística indicada sobre ese estado.
    public static int calcular(int heuristica, String estado, String objetivo) {
        if (heuristica == DISTANCIA_MANHATTAN) {
            return distanciaManhattan(estado, objetivo);
        }
        return fichasFueraDeLugar(estado, objetivo);
    }

    public static String nombre(int heuristica) {
        if (heuristica == DISTANCIA_MANHATTAN) {
            return "distancia Manhattan";
        }
        return "fichas fuera de lugar";
    }
}
