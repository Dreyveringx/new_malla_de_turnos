/** Descarga la plantilla .xlsx servida desde /public (columnas reales + diseño). */
export async function descargarPlantillaImportacionCatalogos(): Promise<string> {
  const fileName = 'Plantilla_Importacion_Catalogos_Malla_Turnos.xlsx';
  const res = await fetch(`/${fileName}`);
  if (!res.ok) {
    throw new Error(`No se encontró la plantilla (${res.status})`);
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  a.click();
  URL.revokeObjectURL(url);
  return fileName;
}
