"""Junta la descarga, el corte, las predicciones, las métricas y las gráficas."""

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from serie_temporal.api_client import obtener_datos
from serie_temporal.evaluation import mae, rmse
from serie_temporal.model import DIAS_PREVIOS, armar_ejemplos, entrenar_modelo, prediccion_persistencia
from serie_temporal.preprocessing import cortar_serie, preparar_tabla

SALIDA = Path(__file__).resolve().parent / "output"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    datos = obtener_datos()
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "respuesta_api.json").write_text(
        json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    tabla = preparar_tabla(datos)
    # El corte se calcula antes de predecir, para entrenar solo con el primer 80 %.
    corte = int(len(tabla) * 0.8)

    tabla["persistencia"] = prediccion_persistencia(tabla["temperatura"])
    entradas, salidas, posiciones = armar_ejemplos(tabla["temperatura"])

    # posiciones < corte: el día a predecir todavía está en el entrenamiento.
    en_entrenamiento = posiciones < corte
    modelo = entrenar_modelo(entradas[en_entrenamiento], salidas[en_entrenamiento])

    tabla["regresion"] = float("nan")
    tabla.loc[posiciones, "regresion"] = modelo.predict(entradas)
    entrenamiento, prueba = cortar_serie(tabla)

    real = prueba["temperatura"]
    mae_persistencia = mae(real, prueba["persistencia"])
    rmse_persistencia = rmse(real, prueba["persistencia"])
    mae_regresion = mae(real, prueba["regresion"])
    rmse_regresion = rmse(real, prueba["regresion"])

    tabla[["fecha", "temperatura"]].to_csv(SALIDA / "serie_limpia.csv", index=False)
    _graficas(tabla, corte, mae_persistencia, rmse_persistencia, mae_regresion, rmse_regresion)

    informe = {
        "dias": len(tabla),
        "entrenamiento_hasta": str(entrenamiento["fecha"].iloc[-1].date()),
        "prueba_desde": str(prueba["fecha"].iloc[0].date()),
        "dias_entrenamiento": len(entrenamiento),
        "dias_prueba": len(prueba),
        "MAE_persistencia": round(mae_persistencia, 4),
        "RMSE_persistencia": round(rmse_persistencia, 4),
        "MAE_regresion": round(mae_regresion, 4),
        "RMSE_regresion": round(rmse_regresion, 4),
        "intercepto": round(float(modelo.intercept_), 4),
        "pesos_del_mas_viejo_al_mas_reciente": [round(float(peso), 4) for peso in modelo.coef_],
    }
    (SALIDA / "metricas.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Días: {len(tabla)}")
    print(f"Entrenamiento: {len(entrenamiento)} días, hasta {informe['entrenamiento_hasta']}")
    print(f"Prueba: {len(prueba)} días, desde {informe['prueba_desde']}")
    print(f"Persistencia: MAE {informe['MAE_persistencia']} | RMSE {informe['RMSE_persistencia']}")
    print(f"Regresión ({DIAS_PREVIOS} días atrás): MAE {informe['MAE_regresion']} | RMSE {informe['RMSE_regresion']}")
    print(f"Intercepto: {informe['intercepto']}")
    print(f"Pesos (del día más viejo al de ayer): {informe['pesos_del_mas_viejo_al_mas_reciente']}")
    print(f"Gráficas en: {SALIDA}")


def _graficas(tabla, corte, mae_persistencia, rmse_persistencia, mae_regresion, rmse_regresion):
    fecha_corte = tabla["fecha"].iloc[corte]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(tabla["fecha"], tabla["temperatura"], color="#1f4e79")
    ax.axvline(fecha_corte, color="gray", linestyle="--", label="Inicio de la prueba")
    ax.set_title("Temperatura media diaria en Manizales")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / "serie_completa.png", dpi=120)
    plt.close(fig)

    prueba = tabla.iloc[corte:]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(prueba["fecha"], prueba["temperatura"], label="Real", color="black", linewidth=2)
    ax.plot(prueba["fecha"], prueba["persistencia"], label="Persistencia (ayer)", linestyle="--")
    ax.plot(prueba["fecha"], prueba["regresion"], label="Regresión lineal")
    ax.set_title("Días de prueba: real y predicciones")
    ax.set_ylabel("Temperatura (°C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / "prediccion_vs_real.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([-0.15, 0.85], [mae_persistencia, mae_regresion], width=0.3, label="MAE")
    ax.bar([0.15, 1.15], [rmse_persistencia, rmse_regresion], width=0.3, label="RMSE")
    ax.set_xticks([0, 1], ["Persistencia", "Regresión lineal"])
    ax.set_ylabel("Error (°C)")
    ax.set_title("Error en los días de prueba")
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA / "metricas.png", dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
