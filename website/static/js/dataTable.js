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

    let headers = [];
    $('#dataTable thead th').each(function (index) {
        if (index < $('#dataTable thead th').length - 1) {
            headers.push($(this).text());
        }
    });
    csv.push(headers.join(","));

    rows.each(function (row) {
        let rowData = [];
        for (let i = 0; i < row.length - 1; i++) {
            rowData.push(row[i]);
        }
        csv.push(rowData.join(","));
    });

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


$('#excelButton').click(function () {
    exportTableToExcel('data.xlsx');
});


function exportTableToExcel(filename) {
    let rows = table.rows({ search: 'applied' }).data();

    let headers = [];
    $('#dataTable thead th').each(function (index) {
        if (index < $('#dataTable thead th').length - 1) {
            headers.push($(this).text());
        }
    });

    let data = [];
    data.push(headers);

    rows.each(function (row) {
        let rowData = [];
        for (let i = 0; i < row.length - 1; i++) {
            rowData.push(row[i]);
        }
        data.push(rowData);
    });

    let ws = XLSX.utils.aoa_to_sheet(data);

    let wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

    XLSX.writeFile(wb, filename);
}


$('#copyButton').click(function () {
    copyTableToClipboard();
});


function copyTableToClipboard() {
    let rows = table.rows({ search: 'applied' }).data();

    let headers = [];
    $('#dataTable thead th').each(function (index) {
        if (index < $('#dataTable thead th').length - 1) {
            headers.push($(this).text());
        }
    });

    let data = [];
    data.push(headers);

    rows.each(function (row) {
        let rowData = [];
        for (let i = 0; i < row.length - 1; i++) {
            rowData.push(row[i]);
        }
        data.push(rowData);
    });

    let clipboardText = data.map(row => row.join("\t")).join("\n");

    navigator.clipboard.writeText(clipboardText).then(() => {
        alert("Copy thành công!");
    }).catch(err => {
        console.error("Failed to copy table data: ", err);
    });
}
  