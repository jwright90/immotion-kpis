let sortDirection = false;
let objTableData = Object.entries(tableData);

window.onload = () => {
    loadTableData(tableData);
};

function loadTableData(tableData) {
    const tableBody = document.getElementById('tableData');
    let dataHTML = '';

    for(let [site, table_info] of obj_tableData) {
        dataHTML += `<tr>   <td>${site}</td>
                            <td>${table_info.total_revenue}</td>
                            <td>${table_info.headsets}</td>
                            <td>${table_info.revenue_per_headset}</td>
                            <td>${table_info.partner_share}</td>
                            <td>${table_info.operations_cost}</td>
                            <td>${table_info.contribution}</td>
                            <td>${table_info.contribution_per_headset}</td>
                            <td>${table_info.margin}%</td>
                    </tr>` ;
    }

    tableBody.innerHTML = dataHTML;
}

function sortColumn(columnName) {
    const dataType = typeof obj_tableData[0][1][columnName];
    console.log(dataType);
    sortDirection = !sortDirection;

    switch(dataType) {
        case 'number':
        sortNumberColumn(sortDirection, columnName);
        break;
    }

    loadTableData(obj_tableData);
}

function sortNumberColumn(sort, columnName) {
    obj_tableData = obj_tableData.sort((p1, p2) => {
        return sort ? p1[1][columnName] - p2[1][columnName] : p2[1][columnName] - p1[1][columnName] 
    });
}



/*
function sortByCustomer() {
    const dataType = typeof obj_tableData[0];
    console.log(dataType);
    sortDirection = !sortDirection;

    switch(dataType) {
        case 'string':
        sortCustomerColumn(sortDirection);
        break;
}

function sortCustomerColumn(sort) {
    obj_tableData = obj_tableData.sort((p1, p2) => {
        return sort ? p1 - p2 : p2 - p1
    });
}
*/