// Когда HTML-документ готов
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var infoMessage = $("#jq-notification");


    // =========================================

    // Получаем параметр q из URL
    const query = new URLSearchParams(window.location.search).get('q');

    if (query) {
        // Заполняем поле поиска значением из URL
        $('input[name="q"]').val(query);

        // Выполняем поиск с полученным значением
        performSearch(query);
    }

    // =========================================



    // Открыть модальное окно выбора подборки пользователя для добавления
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });



    // =========================================



    // Сделать кликабельным строчку таблицы с классом '.clickable-row', кроме иконок удаления и добавления в коллекцию
    document.querySelectorAll('.clickable-row').forEach(row => {
        row.addEventListener('click', function (event) {
            // Проверяем, не был ли клик по элементу с классом 'delete-icon' или 'add-to-user-collection'
            if (!event.target.closest('.delete-icon') && !event.target.closest('.add-to-user-collection-button')) {
                window.location.href = this.getAttribute('data-href');
            }
        });
    });



    // ==========================================================================


    // Добавление категорий пользователя

    // Обработчик клика на кнопку создания категории если он есть на странице

    const formElement = document.getElementById('create_category_form');

    if (formElement) {
        formElement.addEventListener('submit', function (e) {
            e.preventDefault();  // Предотвращаем стандартное поведение формы

            // Получаем значение категории из поля ввода
            let categoryName = this.category_name.value;

            if (categoryName === '') {
                // Сообщение
                infoMessage.html("Введите название категории которую хотите создать");
                infoMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);
                return;
            }

            // Отправляем AJAX-запрос на создание новой категории
            $.ajax({
                url: $('#create_category_form').attr('action'),  // Получаем URL из атрибута формы
                method: 'POST',
                data: {
                    category_name: categoryName,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()  // Передаем CSRF токен
                },
                success: function (response) {
                    // Очищаем поле ввода
                    $('#newCategoryName').val('');

                    // Сообщение
                    infoMessage.html(response.message);
                    infoMessage.fadeIn(400);
                    // Через 7сек убираем сообщение
                    setTimeout(function () {
                        infoMessage.fadeOut(400);
                    }, 7000);
                    
                    // Меняем содержимое категорий на ответ от Django (новый отрисованный HTML)
                    var tileContainer = $("#include-list-categories-place");
                    tileContainer.html(response.collections);  // Обновляем контейнер с категориями

                },
                error: function (xhr, status, error) {
                    console.error('Ошибка при создании категории:', error);
                }
            });
        });
    }

    // ==========================================================================


    // Удаление категории пользователя

    // Обработчик клика на значок корзины
    $(document).on('click', '.cart-icon', function (e) {
        e.preventDefault(); // Предотвращаем стандартное действие

        // Получаем данные из атрибутов значка корзины
        var categoryName = $(this).data('category');
        var actionUrl = $(this).attr("href");

        // Отправляем AJAX POST запрос
        $.ajax({
            url: actionUrl,
            method: 'POST',
            data: {
                category_name: categoryName,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // Передаем CSRF токен
            },
            success: function (response) {
                // Сообщение
                infoMessage.html(response.message);
                infoMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);

                // Меняем содержимое категорий на ответ от Django (новый отрисованный HTML)
                var tileContainer = $("#include-list-categories-place");
                tileContainer.html(response.collections);  // Обновляем контейнер с категориями
            },
            error: function (xhr, status, error) {
                // Обрабатываем ошибку
                console.error('Ошибка при удалении категории:', error);
            }
        });
    });


    // ==========================================================================
    // Удаление токена из подборки

    $(document).on('click', '.delete-icon', function (e) {
        e.preventDefault();

        var poolAddress = $(this).data('pool-address');
        var collectionName = $(this).data('category');
        var actionUrl = $(this).data('action');

        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: {
                pool_address: poolAddress,
                collection_name: collectionName,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                // Сообщение
                infoMessage.html(response.message);
                infoMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);

                // location.reload(); // Обновляем страницу после удаления

                // Удаление строки с нужным data-href
                var poolAddress = response.pool_address;
                $('tr[data-pool-address-del=' + poolAddress + ']').remove();
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при удалении пула:', error);
            }
        });
    });


    // ==========================================================================


    // Добавление токена в подборку
    // Для кнопки "+" в new-pairs
    $(document).on("click", ".add-to-user-collection-button", function (e) {
        e.preventDefault();
    
        var poolAddress = $(this).data("pool-address");
    
        // Устанавливаем значение в модальном окне
        $("#exampleModal").data("pool-address", poolAddress);
    
        $("#exampleModal").modal('show');  // Открываем модальное окно
    });

    
    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-user-collection", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Получаем address пула из атрибута data-addres
        var address = $(this).data("address");
        // Если адрес отсутствует, получаем его из модального окна
        if (!address) {
            address = $("#exampleModal").data("pool-address");
        }

        // Получаем название категории пула из атрибута data-category
        var collection_name = $(this).data("collection");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_collection_url = $(this).attr("href");

        // Получаем элемент с нужным data-collection-name
        var collectionCountElement = $(".collection_count[data-collection-name='" + collection_name + "']");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_collection_url,
            data: {
                pool_address: address,
                collection_name: collection_name,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Получаем текущее значение и увеличиваем его на 1
                var currentCount = parseInt(collectionCountElement.text(), 10);

                if (!isNaN(currentCount)) {
                    collectionCountElement.text(currentCount + 1);
                }

                // Сообщение
                infoMessage.html(data.message);
                infoMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);
            },
            error: function (xhr, status, error) {
                var response = xhr.responseJSON;
                
                // Если есть JSON-ответ от сервера
                if (response && response.message) {
                    infoMessage.html(response.message); // Выводим сообщение об ошибке из JSON
                } else {
                    // Иначе выводим общее сообщение об ошибке
                    infoMessage.html("Произошла ошибка при добавлении в подборку. Попробуйте снова.");
                }
    
                // Показать сообщение об ошибке
                infoMessage.fadeIn(400);
    
                // Через 7 секунд убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);

                console.error("Ошибка при добавлении товара в корзину");
            },
        });
    });



    // =========================================


    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }


    // ==========================================

    // Открытие и закрытие модального окна результатов поиска

    function openModal() {
        var myModal = new bootstrap.Modal(document.getElementById('searchModal'));
        myModal.show();
    }
    

    function closeModal() {
        document.getElementById('searchModal').style.display = 'none';
    }



    // ==========================================



    // Поиск
    // document.addEventListener('DOMContentLoaded', function () {
    //     const query = new URLSearchParams(window.location.search).get('q');
        
    //     console.log(query); // Проверка значения параметра 'q'
    //     console.log('LNNNNNNOOOL'); // Проверка, что этот лог появляется
    
    //     if (query) {
    //         document.querySelector('input[name="q"]').value = query;
    //         performSearch(query); // Выполняем поиск
    //     }
    // });
    
    
    
    function performSearch(query) {

        // Отправляем AJAX-запрос с поисковым запросом
        $.ajax({
            url: $('#searchForm').attr('action'),
            method: 'GET',
            data: {
                q: query,
            },
            success: function (response) {
                // Меняем содержимое контейнера с результатами поиска
                var tileContainer = $("#searchResults");
                tileContainer.html(response.q_results);  // Обновляем контейнер с результатами поиска
                openModal();  // Открываем модальное окно
            },
            error: function (xhr, status, error) {
                var response = xhr.responseJSON;
                // Сообщение
                infoMessage.html(response.message);
                infoMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    infoMessage.fadeOut(400);
                }, 7000);

                console.error('Ошибка при выполнении поиска:', error);
            }
        });
    }
    
    document.getElementById('searchForm').addEventListener('submit', function (e) {
        e.preventDefault();  // Предотвращаем стандартное поведение отправки формы
    
        let query = this.q.value;  // Получаем значение поля ввода
    
        if (query === '') {
            // Сообщение
            infoMessage.html("Запрос не может быть пустым");
            infoMessage.fadeIn(400);
            // Через 7сек убираем сообщение
            setTimeout(function () {
                infoMessage.fadeOut(400);
            }, 7000);
            return;
        }
    
        // Обновляем URL
        history.pushState(null, '', `?q=${encodeURIComponent(query)}`);
    
        // Выполняем поиск
        performSearch(query);
    });
    
    function openModal() {
        var searchModal = new bootstrap.Modal(document.getElementById('searchModal'), {
            keyboard: false
        });
        searchModal.show();
    }
    
    

});
