if(window.location.href.split('/').pop() == "home"){
    const week = ["日", "月", "火", "水", "木", "金", "土"];
    const today = new Date();
    let showDate = new Date(today.getFullYear(), today.getMonth(), 1);

    window.onload = function () {
        showProcess(today, calendar);
    };
    function prev(){
        showDate.setMonth(showDate.getMonth() - 1);
        showProcess(showDate);
    }

    function next(){
        showDate.setMonth(showDate.getMonth() + 1);
        showProcess(showDate);
    }

    function showProcess(date) {
        let year = date.getFullYear();
        let month = date.getMonth();
        document.querySelector('#c_header').innerHTML = year + "年 " + (month + 1) + "月";

        let calendar = createProcess(year, month);
        document.querySelector('#calendar').innerHTML = calendar;
    }

    function createProcess(year, month) {
        let calendar = "<table><tr class='dayOfWeek'>";
        for (let i = 0; i < week.length; i++) {
            calendar += "<th>" + week[i] + "</th>";
        }
        calendar += "</tr>";

        let count = 0;
        let startDayOfWeek = new Date(year, month, 1).getDay();
        let endDate = new Date(year, month + 1, 0).getDate();
        let lastMonthEndDate = new Date(year, month, 0).getDate();
        let row = Math.ceil((startDayOfWeek + endDate) / week.length);

        for (let i = 0; i < row; i++) {
            calendar += "<tr>";
            for (let j = 0; j < week.length; j++) {
                if (i == 0 && j < startDayOfWeek) {
                    calendar += "<td class='disabled'>" + (lastMonthEndDate - startDayOfWeek + j + 1) + "</td>";
                } else if (count >= endDate) {
                    count++;
                    calendar += "<td class='disabled'>" + (count - endDate) + "</td>";
                } else {
                    count++;
                    if(year == today.getFullYear()
                    && month == (today.getMonth())
                    && count == today.getDate()){
                        calendar += "<td class='today'>" + count + "</td>";
                    } else {
                        calendar += "<td>" + count + "</td>";
                    }
                }
            }
            calendar += "</tr>";
        }
        return calendar;
    }
}

if(window.location.href.split('/').pop() == "task_practice_list"){
    window.addEventListener('DOMContentLoaded', (event) => {
        const labels = document.querySelectorAll('label');
        const labelCount = labels.length;
        
        let name = [];
        let goalname = [];
        labels.forEach((label) => {
            const su = label.className.slice(-1);
            name.push('botton' + su);
            goalname.push('task_goal' + su);
        });
        
        for(let i = 0;i < labelCount;i++){
            const checkebox = document.getElementById(name[i]);
            const element = document.getElementById(goalname[i]);

            function toggleElementVisibility(){
                if(checkebox.checked){
                    element.style.display = "block";
                }else{
                    element.style.display = "none";
                }
            }
            checkebox.addEventListener("change",toggleElementVisibility);
            toggleElementVisibility();
        }
    });

}

if(window.location.href.split('/').pop() == "task_practice_q1"){
    /***** ドラッグ開始時の処理 *****/
    function f_dragstart(event){
        //ドラッグするデータのid名をDataTransferオブジェクトにセット
        event.dataTransfer.setData("text", event.target.id);
    }
    
    /***** ドラッグ要素がドロップ要素に重なっている間の処理 *****/
    function f_dragover(event){
        //dragoverイベントをキャンセルして、ドロップ先の要素がドロップを受け付けるようにする
        event.preventDefault();
    }
    
    /***** ドロップ時の処理 *****/
    function f_drop(event){
        //ドラッグされたデータのid名をDataTransferオブジェクトから取得
        var id_name = event.dataTransfer.getData("text");
        //id名からドラッグされた要素を取得
        var drag_elm =document.getElementById(id_name);
        //ドロップ先にドラッグされた要素を追加
        event.currentTarget.appendChild(drag_elm);
        //エラー回避のため、ドロップ処理の最後にdropイベントをキャンセルしておく
        event.preventDefault();
    }
}