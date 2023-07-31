const getURL = (current_url, page, order = undefined) => {

    let ini = 0
    let fin = 0

    let URL = current_url
    
    const page_param = current_url.includes('page')
    const order_param = current_url.includes('order')
    
    if(page_param && order_param){
        ini = current_url.indexOf('=')
        fin = current_url.indexOf('&')
        page = (page > 0) ? page : current_url.substring(ini + 1, fin)
        
        ini = current_url.indexOf('=', fin)
        fin = current_url.length
        order = (order != undefined) ? order : current_url.substring(ini + 1, fin)
    
        URL = `?page=${page}&order=${order}`
    }
    else if(page_param && !order_param){
        ini = current_url.indexOf('=', fin)
        fin = current_url.length
        page = (page > 0) ? page : current_url.substring(ini + 1, fin)

        URL = (order != undefined) ? `?page=${page}&order=${order}` : `?page=${page}`
    }
    else if(!page_param && order_param){
        ini = current_url.indexOf('=', fin)
        fin = current_url.length
        order = (order != undefined) ? order : current_url.substring(ini + 1, fin)

        URL = (page > 0) ? `?page=${page}&order=${order}` : `?order=${order}`
    }
    else{
        if(page > 0) URL = `?page=${page}`
        if(order != undefined) URL = `?order=${order}`
    }

    return URL
}