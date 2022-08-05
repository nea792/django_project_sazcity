
updatebtns = document.getElementsByClassName('update-cart')
showRatesOfComments = document.getElementsByClassName('show_rate')

for(var i=0;i< updatebtns.length;i++){
    updatebtns[i].addEventListener('click',function(){

        
        var action = this.dataset.action
        if (action ==="addOrder")
        {   var productId = this.dataset.product
            var value = $(".procuct_cover .choice_color input[type=radio][name=color]:checked").val()
            if (!value){
                alert("رنگ را انتخاب کنید")
            }
            else{
                addUserOrder(productId,action,value)
            }
        }
        else
        {
            var orderItemId = this.dataset.item
            updateUserOrder(orderItemId,action)

        }
    })
}

for(var i=0; i< showRatesOfComments.length;i++){
    
    var value = showRatesOfComments[i].dataset.rate
    spans_rate = showRatesOfComments[i].getElementsByTagName('span')
    for (var j = 0; j < value ; j++) {
        var currentEl = spans_rate[j];
        currentEl.style.color = '#f70';
    }
}

function addUserOrder(productId,action,value)
{
    if (user==='AnonymousUser'){
        alert("شما هنوز وارد حساب کاربری خود نشده اید")
    }
    else{
        var url='/product/add_order'
        fetch(url,{
            method:'POST',
            headers : {
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId':productId, 'action':action, 'colorValueId':value })
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            console.log('data',data)
            location.reload()
        })
    }
}

function updateUserOrder(orderItemId, action,)
{
    var url='/product/update_order'
    fetch(url,{
        method:'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
         body:JSON.stringify({'orderItemId':orderItemId, 'action':action })
    })
    .then((response)=>{
        return response.json()
    })
    
    .then((data)=>{
        console.log('data',data)
        location.reload()
    })
}

$(document).ready(function(){
    $('.reply_btn').click(function(){
        $(this).next('.reply_form').toggle()
    })

    $('.toggle_reply').click(function(){
        $(this).next('.reply').toggle()
    })
})