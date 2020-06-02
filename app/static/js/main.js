$(document).ready(function() {
    Chart.Scatter(document.getElementById('ICD_count_chart'));
    new Chart(document.getElementById('death_pie_chart'), {type:"pie"});
    Chart.Scatter(document.getElementById('inpatient_chart'));
    setSearchBtn();
});

function setSearchBtn(){
    $("#search_patient_btn").click(function(){ 
        getPatientData($("#patient_id_input").val());
        
    });
}

function getPatientData(id){
    //test id : fff2ecdf8a0234c105986a3b4a45ae5b
    $.post("set_patient", {"patientid":id}, function(){
        $.post("personal_data", function(data){
            alert(data);
            var result = jQuery.parseJSON(data);
            //set first five char as patient name
            $("#patient_name").text(result[0].id.substr(0,5));
            //set gender
            if(result[0].gender == "M"){
                $("#patient_gender").text("男性");
                $("#left_menu_background").attr("style", "background-color:rgb(200,200,255)");
            }
            else{
                $("#patient_gender").text("女性");
                $("#left_menu_background").attr("style", "background-color:rgb(255,200,200)");
            }
            //set birthday
            $("#patient_birthday").text(result[0].birthdate)
            getInpatient($("#patient_id_input").val());
        getDeathRate();
        getICDCount();
        });
    });
}

function getInpatient(id){
    $.post("inpatient", {"patientid":id}, function(data){
        var result = jQuery.parseJSON(data);
        $.post("inpatient_mean",function(data){
            var result_mean = jQuery.parseJSON(data);
            var ctx = document.getElementById('inpatient_chart');
            window.myScatter = Chart.Scatter(ctx, {
                data: {
                    datasets: [{
                        label: '我的住院周期',
                        backgroundColor: "rgba(255, 0, 0, 0.5)",
                        borderColor: 'rgba(255, 99, 132, 0.5)',
                        data: normalizeInpatientData(result),
                        showLine: true,
                        fill: false,
                        tension: 0,
                        pointRadius:10,
                        pointHoverRadius:15,
                    }, {
                        label: '全體住院周期平均',
                        backgroundColor: "rgba(0, 0, 255, 0.5)",
                        borderColor: 'rgba(54, 162, 235, 0.5)',
                        data: normalizeInpatientData(result_mean),
                        fill: false,
                        showLine: true,
                        tension: 0,
                        pointStyle: "triangle",
                        pointRadius:10,
                        pointHoverRadius:15,
                    }]
                }}
            );
        })
    })
}

function normalizeInpatientData(data){
    var result = [];
    var i=0;
    for(i=0; i<data.x.length; i++)
    {
        result.push({"x":data.x[i], "y":data.y[i]});
    }
    return result;
}

function getDeathRate(){
    $.post("shorterm_death_prob", function(data){
        var ctx = document.getElementById('death_pie_chart');

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Dead', 'Alive'],
                datasets: [{
                    data: [data, 1-data],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                    ],
                    fill: false,
					borderDash: [5, 5],
                }]
            }
        });
    })
}

function getICDCount(){
    var datas = [];
    var zeroFlag = false;
    $.post("icd_card", function(data){
        data = jQuery.parseJSON(data);
        
        $.each(data, function(_, values){
            if(values.y != 0)
                zeroFlag = true;
            if(zeroFlag)
                datas.push(values);
        });

        var ctx = document.getElementById('ICD_count_chart');
        window.myScatter = Chart.Scatter(ctx, {
            data: {
                datasets: [{
                    label: '我的罹患疾病(種)',
                    backgroundColor: "rgba(255, 0, 0, 0.8)",
                    borderColor: 'rgba(255, 99, 132, 0.8)',
                    data: datas,
                    showLine: true,
                    fill: false,
                    tension: 0,
                    pointRadius: 5,
                    pointHoverRadius: 10
                }]
        }});
    })
}

