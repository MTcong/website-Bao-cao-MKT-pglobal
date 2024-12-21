let table = new DataTable('#dataTable', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    "lengthMenu": [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    // "order": [[0, "desc"]],
    // footerCallback: function(row, data, start, end, display) {
    //     let totalCost = 0;
    //     let totalPhoneNumber = 0;
    //     let totalRevenue = 0;

    //     data.forEach(function(row) {
    //         totalCost += parseFloat(row[1].replace(/[^0-9.-]+/g, "")) || 0;
    //         totalPhoneNumber += parseInt(row[2].replace(/[^0-9.-]+/g, "")) || 0;
    //         totalRevenue += parseFloat(row[4].replace(/[^0-9.-]+/g, "")) || 0;
    //     });

    //     totalCostPerPhone = parseInt(totalCost/totalPhoneNumber) || 0;
    //     totalcpqc = (parseFloat(totalCost/totalRevenue*100) || 0).toFixed(2);
    //     totalroat = (parseFloat(totalRevenue/totalCost) || 0).toFixed(2);

    //     $('#total-cost1').html(totalCost.toLocaleString() + " VND");
    //     $('#total-phoneNumber1').html(totalPhoneNumber.toLocaleString());
    //     $('#total-costPerPhone1').html(totalCostPerPhone.toLocaleString() + " VND");
    //     $('#total-revenue1').html(totalRevenue.toLocaleString() + " VND");
    //     $('#total-cpqc1').html(totalcpqc.toLocaleString()+ "%");
    //     $('#total-roat1').html(totalroat.toLocaleString());
    // },
});


$('#printButton').on('click', function () {
    let printWindow = window.open('', '_blank');
    let title = document.querySelector('#page-title').textContent;

    let table = document.querySelector('#dataTable');
    table.querySelectorAll('tr').forEach(row => {
        let lastCell = row.querySelector('td:last-child, th:last-child');
        if (lastCell) {
            lastCell.remove();
        }
    });
    let tableHtml = table.outerHTML;

    printWindow.document.write(`
        <html>
        <head>
            <title>${title}</title>
            <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            </style>
        </head>
        <body>
            <h2>${title}</h2>
            ${tableHtml}
            <script>
                setTimeout(() => { window.print(); window.close(); }, 500);
            </script>
        </body>
        </html>
    `);
    printWindow.document.close();
});


$('#csvButton').click(function () {
    exportTableToCSV('data.csv');
});


function exportTableToCSV(filename) {
    let csv = [];
    let rows = table.rows({ search: 'applied' }).data();

    // Add table header (excluding the last column)
    let headers = [];
    $('#dataTable thead th').each(function (index) {
        if (index < $('#dataTable thead th').length - 1) { // Exclude the last column
            headers.push($(this).text());
        }
    });
    csv.push(headers.join(","));

    // Add table rows (excluding the last column)
    rows.each(function (row) {
        let rowData = [];
        for (let i = 0; i < row.length - 1; i++) { // Exclude the last column
            rowData.push(row[i]);
        }
        csv.push(rowData.join(","));
    });

    // Convert the CSV string to a Blob with UTF-8 encoding
    let csvString = csv.join("\n");
    let blob = new Blob(["\ufeff" + csvString], { type: 'text/csv;charset=utf-8;' });
    let link = document.createElement("a");
    if (link.download !== undefined) {
        let url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}


$('#pdfButton').click(function () {
    exportTableToPDF('data.pdf');
});


function exportTableToPDF(filename) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
  
    const fontBase64 = 'YOUR_BASE64_ENCODED_FONT_HERE'; // Replace with your base64-encoded font data

    doc.addFileToVFS('Roboto-Regular.ttf', fontBase64);
    doc.addFont('Roboto-Regular.ttf', 'Roboto', 'normal');
    doc.setFont('Roboto'); // Set the custom font for the PDF

    // Fetch headers from the <thead>
    const headers = [];
    $('#dataTable thead th').each(function () {
      headers.push($(this).text()); // Get the text from each <th> in the header
    });
    headers.pop();

    // Fetch data from the table
    const tableData = [];
    $('#dataTable tbody tr').each(function () {
      const rowData = [];
      $(this).find('th').each(function () {
        rowData.push($(this).text()); // Extract the text from each cell
      });
      rowData.pop();
      tableData.push(rowData);
    });
  
    // Customize PDF settings and table structure
    doc.autoTable({
      head: [headers],  // Use the extracted headers from <thead>
      body: tableData,  // Table data
      theme: 'striped', // Optional theme for the table
      styles: {
        font: 'Roboto-Regular', // Use Helvetica font
        fontSize: 12, // Font size for the table
        cellPadding: 3, // Padding in cells
      }
    });
  
    // Save the generated PDF with the provided filename
    doc.save(filename);
}
  
  