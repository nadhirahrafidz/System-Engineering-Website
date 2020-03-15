$('document').ready(function(){

    $('#id_region').find('option').each(function() {
        $(this).attr('hidden',true);
    });
    $('#id_cluster').find('option').each(function() {
        $(this).attr('hidden',true);
    });
      
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

$(function(ready){
    $('#id_country').change(function() {
        observe("#id_country", "#id_region");
        country = $("#id_country option:selected").val();
        get_data(country, 0, 0);
    });

    $('#id_region').change(function() {
        observe("#id_region", "#id_cluster");
        region = $("#id_region option:selected").val();
        get_data(0, region, 0);
    });

    $('#id_cluster').change(function() {
        observe("#id_region", "#id_cluster");
        cluster = $("#id_cluster option:selected").val();
        get_data(0, 0, cluster);
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