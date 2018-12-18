$(document).ready(function(){

    $('#stop-words').click(function(){
        if($(this).is(':checked'))
        {
            this.value = true
            $(this).siblings(".text-input").prop('disabled', false);
        }
        else
        {
            this.value = false
            $(this).siblings(".text-input").prop('disabled', true);
        }
    });

    $('#lemmatize').click(function(){
        if($(this).is(':checked'))
        {
            this.value = true
        }
        else
        {
            this.value = false
        }
    });
});