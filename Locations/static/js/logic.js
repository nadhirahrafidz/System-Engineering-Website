$('document').ready(function(){
    $('#QA').attr('hidden', true);
    $('#div_id_answerNext').attr('hidden', true);
    $('#id_answerNext').find('option').each(function() {
        $(this).attr('hidden',true)
    });
    observe("#id_currentQ","#id_answerNext")  
})

$('#id_relation').change(function() {
    var relation = $('#id_relation').val()
    if(relation == '')
    {
        $('#QA').attr('hidden', true);
        $('#div_id_answerNext').attr('hidden', true);
    }
    else if(relation == 'NEXT')
    {
        $('#QA').attr('hidden', true);
        $('#div_id_answerNext').removeAttr('hidden');
    }
    else if(relation == 'AND' || relation == 'OR')
    {
        $('#QA').removeAttr('hidden');
        $('#div_id_answerNext').attr('hidden', true);
        observe("#id_form-0-conditionalQuestion","#id_form-0-conditionalAnswer")  
    }
})

function observe(observedElement, changedElement) 
{
    var chosenQuestion = $(observedElement).val()
    var qnn = $('#questionnaire_id').text()
    $.ajax({
        url: '/questionnaires/ajax/',
        data: {
            'question_id' : chosenQuestion,
            'questionnaire_id' : qnn,
        },
        success: function(response) {
            $(changedElement).find('option').each(function() {
                $(this).attr('hidden',true)
            });
            var answers = response.answers
            $(changedElement).find('option').each(function() {
                if(answers.indexOf($(this).val()) !== -1) {
                    $(this).removeAttr('hidden')
                }
            })
        }
    })
}

$("#id_currentQ").change(function() 
{
    observe("#id_currentQ","#id_answerNext")
})

$('.qrelForm').change(function(e) {
    if((e.target.id).includes("Question"))
    {
        var targetQ = "#"+e.target.id;
        var targetA = targetQ.replace("conditionalQuestion", "conditionalAnswer");
        observe(targetQ, targetA);
    }
});

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}

$('#add_more').click(function() {
    cloneMore('div.table:last', 'form');
});


// $('#id_currentQ').change(function() {
//     var chosenQuestion = $('#id_currentQ').val()
//     var qnn = $('#questionnaire_id').text()
//     $.ajax({
//         url: '/questionnaires/ajax/',
//         data: {
//             'question_id' : chosenQuestion,
//             'questionnaire_id' : qnn,
//         },
//         success: function(response) {
//             // Remove previous answers
//             $("#id_answerNext option").remove()
//             var answers = response.answers
//             var length = answers.length
//             for(var i = 0; i < length; i++)
//             {
//                 var [string, id] = answers[i]
//                 $("#id_answerNext").append(new Option(string, id));
//             }
//         }
//     })
// })


// Original Observe

// function observe(observedElement, changedElement) 
// {
//     var chosenQuestion = $(observedElement).val()
//     var qnn = $('#questionnaire_id').text()

//     $.ajax({
//         url: '/questionnaires/ajax/',
//         data: {
//             'question_id' : chosenQuestion,
//             'questionnaire_id' : qnn,
//         },
//         success: function(response) {
//             $(changedElement+" option").remove()
//             var answers = response.answers
//             var length = answers.length
//             for(var i = 0; i < length; i++)
//             {
//                 var [string, id] = answers[i]
//                 $(changedElement).append(new Option(string, id));
//             }
//         }
//     })
// }