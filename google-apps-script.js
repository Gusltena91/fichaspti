// ============================================================
// Google Apps Script — Webhook para recibir leads de fichas técnicas
// ============================================================
// INSTRUCCIONES:
// 1. Ve a https://script.google.com y crea un nuevo proyecto
// 2. Pega este código
// 3. Ejecuta la función "setup" una vez para crear la hoja
// 4. Deploy > New deployment > Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Copia la URL del deployment y pégala en index.html (GOOGLE_SCRIPT_URL)
// ============================================================

var SHEET_NAME = 'Leads Fichas Técnicas';

function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  sheet.getRange(1, 1, 1, 8).setValues([[
    'Fecha', 'Producto', 'Nombre', 'Email', 'Empresa', 'Teléfono', 'Estado', 'Fuente'
  ]]);
  sheet.getRange(1, 1, 1, 8).setFontWeight('bold');
  sheet.setFrozenRows(1);
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      setup();
      sheet = ss.getSheetByName(SHEET_NAME);
    }

    sheet.appendRow([
      data.fecha || new Date().toISOString(),
      data.producto || '',
      data.nombre || '',
      data.email || '',
      data.empresa || '',
      data.telefono || '',
      data.estado || '',
      data.fuente || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', message: 'Webhook activo' }))
    .setMimeType(ContentService.MimeType.JSON);
}
