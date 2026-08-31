

const burger = document.querySelector('.burger');
const menu = document.querySelector('.header__links');
const overlay = document.querySelector('.menu-overlay');


function toggleMenu(){

    burger.classList.toggle('active');
    menu.classList.toggle('active');
    overlay.classList.toggle('active');

    document.body.classList.toggle('lock');

}

burger.addEventListener('click', toggleMenu);
overlay.addEventListener('click', toggleMenu);


document.querySelectorAll('.header__link').forEach(link=>{

    link.addEventListener('click',()=>{

        burger.classList.remove('active');
        menu.classList.remove('active');
        overlay.classList.remove('active');

        document.body.classList.remove('lock');

    });

});


document.addEventListener('DOMContentLoaded', () => {
    const section = document.querySelector('.disciplines');

    if (!section) return;

    const wrapper = section.querySelector('.disciplines__items-wrapper');
    const items = section.querySelectorAll('.disciplines__item');
    const button = section.querySelector('.disciplines__toggle');

    const visibleCount = Number(section.dataset.visible) || 3;

    const getClosedHeight = () => {
        const visibleItems = [...items].slice(0, visibleCount);

        // На мобильном карточки идут друг под другом
        if (window.innerWidth <= 768) {
            return visibleItems.reduce(
                (height, item) => height + item.offsetHeight,
                0
            ) + (visibleItems.length - 1) * 20;
        }

        // На десктопе первые 3 карточки находятся в одной строке
        return Math.max(
            ...visibleItems.map(item => item.offsetHeight)
        );
    };

    const setClosedHeight = () => {
        wrapper.style.maxHeight = `${getClosedHeight()}px`;
    };

    // Начальное состояние — только 3 карточки
    setClosedHeight();

    button.addEventListener('click', () => {
        const isOpen = section.classList.toggle('is-open');

        if (isOpen) {
            wrapper.style.maxHeight = `${wrapper.scrollHeight}px`;
            button.textContent = 'СКРЫТЬ ДИСЦИПЛИНЫ';
        } else {
            wrapper.style.maxHeight = `${getClosedHeight()}px`;
            button.textContent = 'ВСЕ ДИСЦИПЛИНЫ';
        }
    });

    window.addEventListener('resize', () => {
        if (section.classList.contains('is-open')) {
            wrapper.style.maxHeight = `${wrapper.scrollHeight}px`;
        } else {
            setClosedHeight();
        }
    });
});