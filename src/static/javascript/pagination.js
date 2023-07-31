const max_page = page['max_page']
const num_page = page['num_page']
const num_nav_buttons = page['num_nav_buttons']
const pagination = document.getElementById('pagination')

const appendLeftButton = (num_page) => {
    const pageNumber = document.createElement('a')

    pageNumber.innerHTML = "&laquo;"
    pageNumber.className = "page-button"
    pageNumber.href = (num_page > 1) ? `?page=${num_page - 1}` : "?page=1"

    pagination.appendChild(pageNumber)
}

const appendNeutralButton = () => {
    const pageNumber = document.createElement('a')
    pageNumber.innerHTML = "..."
    pageNumber.className = "page-neutral"
    pageNumber.href = "#"

    pagination.appendChild(pageNumber)
}

const appendPageButton = (num_page) => {
    const pageNumber = document.createElement('a')
    pageNumber.innerHTML = num_page
    pageNumber.className = "page-button"
    pageNumber.href = `?page=${num_page}`

    pagination.appendChild(pageNumber)
}

const appendPageButtons = (num_page) => {

    if (num_page <= num_nav_buttons){
        appendPageButton(1)
        for (let i = 2; i <= num_nav_buttons; i++) appendPageButton(i)
        appendNeutralButton()
        appendPageButton(max_page)
    }
    else if(num_page > (max_page - num_nav_buttons)){     
        appendPageButton(1)
        appendNeutralButton()
        for (let i = (max_page - num_nav_buttons); i < max_page; i++) appendPageButton(i)
        appendPageButton(max_page)
    }
    else{
        appendPageButton(1)
        appendNeutralButton()
        for (let i = 0; i < (num_nav_buttons - 1); i++) appendPageButton(num_page + i)
        appendNeutralButton()
        appendPageButton(max_page)
    }

}


const appendRightButton = (num_page) => {
    const pageNumber = document.createElement('a')

    pageNumber.innerHTML = "&raquo;"
    pageNumber.className = "page-button"
    pageNumber.href = (num_page < (max_page - 1)) ? `?page=${num_page + 1}` : `?page=${max_page}`

    pagination.appendChild(pageNumber)
}

const navButtons = (num_page) => {
    appendLeftButton(num_page)
    appendPageButtons(num_page)
    appendRightButton(num_page)
}

navButtons(num_page)

// console.log(max_page, num_nav_buttons, num_page)