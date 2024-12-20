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
    // }
});