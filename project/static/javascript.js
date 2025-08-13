document.addEventListener('DOMContentLoaded', function() {
    // show-hide tooltip
    const calculated_list = document.getElementById(`calculated_list`).dataset.length;
    for (let i = 1; i <= calculated_list; i++)
    {
        const tool_tip = document.getElementById(`tool-tip${i}`);
        const tool_tip_display = document.getElementById(`tool-tip-display${i}`);

        tool_tip.onmouseenter = function (){
            tool_tip_display.style.display = "block";
            tool_tip_display.style.position = "absolute";
            tool_tip_display.style.backgroundColor = "#333";
            tool_tip_display.style.color = "#fff";
            tool_tip_display.style.padding = "8px";
            tool_tip_display.style.borderRadius = "4px";
            tool_tip_display.style.fontSize = "14px";
            tool_tip_display.style.zIndex = "1000";
            tool_tip_display.style.marginLeft = "48px";
        };
        tool_tip_display.onmouseleave = function (){
            tool_tip_display.style.display = "none";
        };
    }

    // Calculated table sum
    const tableRows = document.querySelectorAll('#calculatedTable tbody tr');
    let totalAmount = 0;
    let totalUnitDay = 0;
    let totalCostDay = 0;
    let totalCostMonth = 0;
    let totalCostYear = 0;

    if (tableRows.length <= 1) return;

    tableRows.forEach(row => {
        const amountCell = row.children[2];
        const unitDayCell = row.children[3];
        const costDayCell = row.children[4];
        const costMonthCell = row.children[5];
        const costYearCell = row.children[6];
        
        totalAmount += parseFloat(amountCell.textContent.replace(',', ''));
        totalUnitDay += parseFloat(unitDayCell.textContent.replace(',', ''));
        totalCostDay += parseFloat(costDayCell.textContent.replace(',', ''));
        totalCostMonth += parseFloat(costMonthCell.textContent.replace(',', ''));
        totalCostYear += parseFloat(costYearCell.textContent.replace(',', ''));
    });
    
    document.getElementById(`totalAmount`).textContent = totalAmount;
    document.getElementById(`totalUnitDay`).textContent = totalUnitDay.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    document.getElementById(`totalCostDay`).textContent = totalCostDay.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    document.getElementById(`totalCostMonth`).textContent = totalCostMonth.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    document.getElementById(`totalCostYear`).textContent = totalCostYear.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
});