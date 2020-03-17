$('document').ready(function(){
    $('#id_region').find('option').each(function() {
        $(this).attr('hidden',true);
    });
    $('#id_cluster').find('option').each(function() {
        $(this).attr('hidden',true);
    });
    $(function(ready){
        get_data(0,0,0)
        get_patient_data(0,0,0)    
    })
    
    
})

function get_data(countryID, regionID, clusterID)
{
    $.ajax({
        url: '/dashboard/data/',
        data: {
            'countryID' : countryID,
            'regionID'  : regionID,
            'clusterID' : clusterID
        },
        success: function(response) 
        {
            build_pie_chart(response.data)
        }
    });
}

function get_patient_data(countryID, regionID, clusterID)
{
    $.ajax({
        url: '/dashboard/ajax/patient',
        data: {
            'countryID' : countryID,
            'regionID'  : regionID,
            'clusterID' : clusterID
        },
        success: function(response) 
        {
            var i = 0
            $("#patient_table_body").empty();
            for(data in response.data)
            {
                build_row(response.data[i].patient_id, response.data[i].questionnaire_id, response.data[i].questionnaire_name, response.data[i].start);
                i++;
            }
        }
    });
}

function build_row(patientID, questionnaireID, questionnaireString, start)
{
    tableBody = $("#patient_table_body")
    header_open = "<tr>"
    header_close = "</tr>"
    tableBody.append(header_open)
    build_data_in_row(patientID, questionnaireID, questionnaireString, start)
    tableBody.append(header_close)
}

function build_data_in_row(patientID, questionnaireID, questionnaireString, start)
{
    tableBody = $("#patient_table_body") 
    patientID = "<td>" + patientID + "</td>"
    questionnaireID = "<td>" + questionnaireID + "</td>"
    questionnaireString = "<td>" + questionnaireString + "</td>"
    markup = "<td>" + start + "</td>"
    tableBody.append(patientID) 
    tableBody.append(questionnaireID)
    tableBody.append(questionnaireString)
    tableBody.append(markup) 
}


function build_pie_chart(data)
{
    var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Complete', 'Incomplete'],
                    datasets: [{
                        label: '# of Votes',
                        data: data,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 99, 132, 0.2)',
                            
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                }
            });
}

$(function(ready){
    $('#id_country').change(function() {
        observe("#id_country", "#id_region");
        country = $("#id_country option:selected").val();
        get_data(country, 0, 0);
        get_patient_data(country,0,0);
    });

    $('#id_region').change(function() {
        observe("#id_region", "#id_cluster");
        region = $("#id_region option:selected").val();
        get_data(0, region, 0);
        get_patient_data(0, region, 0); 
    });

    $('#id_cluster').change(function() {
        observe("#id_region", "#id_cluster");
        cluster = $("#id_cluster option:selected").val();
        get_data(0, 0, cluster);
        get_patient_data(0, 0, cluster)
    });

});

function observe(observedElement, changedElement) 
{
    var chosenLocation = $(observedElement+' option:selected').val();
    $.ajax({
        url: '/dashboard/ajax/',
        data: {
            'location_id' : chosenLocation,
        },
        success: function(response) {
            $(changedElement).find('option').each(function() {
                $(this).attr('hidden',true)
            });
            var location = response.locations
            $(changedElement).find('option').each(function() {
                if(location.indexOf($(this).val()) !== -1 || $(this).val() === '0') {
                    $(this).removeAttr('hidden')
                }
            });
        }
    });
}
