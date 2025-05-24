document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const themeSwitcherDesktop = document.getElementById('theme-switcher-desktop');
    const themeSwitcherMobile = document.getElementById('theme-switcher-mobile-btn');
    const htmlElement = document.documentElement;

    const bookingModal = document.getElementById('booking-modal');
    const closeBookingModal = document.getElementById('close-booking-modal');
    const openBookingModalHero = document.getElementById('open-booking-modal-hero');
    const openBookingModalCardButtons = document.querySelectorAll('.open-booking-modal-card');
    const carTypeSelect = document.getElementById('car-type');
    const bookingForm = document.getElementById('booking-form');
    const bookingConfirmationMessage = document.getElementById('booking-confirmation-message');

    const carGrid = document.getElementById('car-grid');
    const allCarCards = carGrid ? Array.from(carGrid.children).filter(child => child.classList.contains('car-card-new')) : [];
    const initiallyVisibleCars = 3; // How many cars to show initially on index.html

    const backToTopBtn = document.getElementById('back-to-top-btn');

    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.classList.add('dark');
            if(themeSwitcherDesktop) themeSwitcherDesktop.innerHTML = '<i class="fas fa-sun fa-lg"></i>';
            if(themeSwitcherMobile) themeSwitcherMobile.innerHTML = '<i class="fas fa-sun fa-lg"></i>';
        } else {
            htmlElement.classList.remove('dark');
            if(themeSwitcherDesktop) themeSwitcherDesktop.innerHTML = '<i class="fas fa-moon fa-lg"></i>';
            if(themeSwitcherMobile) themeSwitcherMobile.innerHTML = '<i class="fas fa-moon fa-lg"></i>';
        }
    }

    function toggleTheme() {
        const currentTheme = htmlElement.classList.contains('dark') ? 'dark' : 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(newTheme);
        try {
            localStorage.setItem('theme', newTheme);
        } catch (e) { console.warn('LocalStorage is not available for saving theme preference.'); }
    }

    if(themeSwitcherDesktop) themeSwitcherDesktop.addEventListener('click', toggleTheme);
    if(themeSwitcherMobile) themeSwitcherMobile.addEventListener('click', toggleTheme);

    let savedTheme = 'light';
    try { savedTheme = localStorage.getItem('theme');} catch (e) { /* LocalStorage not available */ }
    if (savedTheme) { applyTheme(savedTheme); }
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) { applyTheme('dark'); }
    else { applyTheme('light'); }

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    function openModal(carType = '') {
        if (bookingModal) {
            if(carTypeSelect && carType) {
                // Find the option with matching text
                for (let i = 0; i < carTypeSelect.options.length; i++) {
                    if (carTypeSelect.options[i].text === carType) {
                        carTypeSelect.selectedIndex = i;
                        break;
                    }
                }
            }
            if(bookingConfirmationMessage) bookingConfirmationMessage.classList.add('hidden'); // Hide confirmation on new open
            bookingModal.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
        }
    }

    function closeModal() {
        if (bookingModal) {
            bookingModal.classList.remove('active');
            document.body.style.overflow = ''; // Re-enable scrolling
        }
    }

    if (openBookingModalHero) {
        openBookingModalHero.addEventListener('click', () => openModal());
    }
    if (openBookingModalCardButtons) {
        openBookingModalCardButtons.forEach(button => {
            button.addEventListener('click', function() {
                const carType = this.getAttribute('data-car-type') || '';
                openModal(carType);
            });
        });
    }
    if (closeBookingModal) {
        closeBookingModal.addEventListener('click', closeModal);
    }
    if (bookingModal) {
        bookingModal.addEventListener('click', function(e) {
            if (e.target === bookingModal) {
                closeModal();
            }
        });
    }

    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(bookingForm);
            const bookingData = {};
            
            // Convert FormData to object
            for (const [key, value] of formData.entries()) {
                bookingData[key] = value;
            }
            
            // Basic validation
            let isValid = true;
            const requiredFields = ['name', 'phone', 'car-type'];
            
            requiredFields.forEach(field => {
                const input = document.getElementById(field);
                const errorSpan = document.getElementById(`${field}-error`);
                
                if (!bookingData[field] || bookingData[field].trim() === '') {
                    isValid = false;
                    input.classList.add('input-error');
                    if (errorSpan) {
                        errorSpan.textContent = 'Bidang ini wajib diisi';
                        errorSpan.classList.remove('hidden');
                    }
                } else {
                    input.classList.remove('input-error');
                    if (errorSpan) {
                        errorSpan.textContent = '';
                        errorSpan.classList.add('hidden');
                    }
                }
            });
            
            if (!isValid) {
                return;
            }
            
            // Format WhatsApp message
            const message = formatWhatsAppMessage(bookingData);
            
            // Encode message for URL
            const encodedMessage = encodeURIComponent(message);
            
            // WhatsApp API URL
            const whatsappUrl = `https://wa.me/6282311113616?text=${encodedMessage}`;
            
            // Open WhatsApp in new tab
            window.open(whatsappUrl, '_blank');
            
            // Close modal
            closeModal();
            
            // Reset form
            bookingForm.reset();
        });
    }

    // Format WhatsApp message
    function formatWhatsAppMessage(data) {
        const message = `*PEMESANAN RENTAL MOBIL*
        
*Informasi Pemesan:*
Nama: ${data.name}
No. HP: ${data.phone}

*Mobil yang Diminati:*
${data['car-type']}

${data.notes ? `*Catatan:*\n${data.notes}` : ''}

Terima kasih telah menghubungi CV. Enam Satu Rentalindo.`;

        return message;
    }

    // This function ensures only 'initiallyVisibleCars' are shown on index.html by default.
    // The "Lihat Semua Mobil" button now navigates to all-cars.html, so no click listener here to show more.
    function updateCarVisibilityHomePage() {
        if (carGrid && (window.location.pathname.endsWith('index.html') || window.location.pathname === '/')) { // Only run on homepage
            allCarCards.forEach((card, index) => {
                if (index < initiallyVisibleCars) {
                    card.classList.remove('car-card-hidden');
                } else {
                    card.classList.add('car-card-hidden');
                }
            });
            const viewAllCarsLink = document.getElementById('view-all-cars-btn');
            if (viewAllCarsLink) {
                 if (allCarCards.length <= initiallyVisibleCars) {
                    viewAllCarsLink.style.display = 'none'; // Hide if not enough cars to warrant "view all"
                } else {
                    viewAllCarsLink.style.display = 'inline-block';
                }
            }
        }
    }
    updateCarVisibilityHomePage(); // Call this for index.html

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            // Check if it's a valid fragment identifier for the current page
            if (targetId && targetId.startsWith('#') && targetId.length > 1 && document.getElementById(targetId.substring(1))) {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                    if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                        mobileMenu.classList.add('hidden');
                    }
                    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active-nav-link'));

                    const desktopClickedLink = document.querySelector(`nav .hidden.md\\:flex a.nav-link[href="${targetId}"]`);
                    const mobileClickedLink = document.querySelector(`#mobile-menu a.nav-link[href="${targetId}"]`);

                    if(desktopClickedLink) desktopClickedLink.classList.add('active-nav-link');
                    if(mobileClickedLink) mobileClickedLink.classList.add('active-nav-link');
                }
            }
            // If it's not a fragment for the current page, let the browser handle it (e.g. link to another page with a fragment)
        });
    });

    const currentYearElement = document.getElementById('currentYear');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }

    const sections = document.querySelectorAll('section[id], header[id]');
    const desktopNavLinks = document.querySelectorAll('nav .hidden.md\\:flex a.nav-link');
    const mobileNavLinks = document.querySelectorAll('#mobile-menu a.nav-link');
    let scrollTimeout;

    function updateActiveNavLinkOnScroll() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            let currentSectionId = 'home'; // Default to home
            let foundCurrent = false;
            const scrollBuffer = window.innerHeight * 0.4; // Adjust buffer as needed

            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;
                if (pageYOffset >= sectionTop - scrollBuffer && pageYOffset < sectionTop + sectionHeight - scrollBuffer) {
                    currentSectionId = section.getAttribute('id');
                    foundCurrent = true;
                }
            });

            // If scrolled to the very bottom, and no section is "current" due to buffer, select the last one
            if (!foundCurrent && (window.innerHeight + window.pageYOffset) >= document.body.offsetHeight - 100) { // 100px buffer from bottom
                if (sections.length > 0) {
                     // Check if the last section is 'hubungi-kami'
                    const lastSection = sections[sections.length -1];
                    if (lastSection.id === 'hubungi-kami') {
                        currentSectionId = 'hubungi-kami';
                    } else if (sections.length > 1 && sections[sections.length-2].id === 'hubungi-kami' && pageYOffset > sections[sections.length-2].offsetTop) {
                        // Special case if footer makes last section not fill screen
                        currentSectionId = 'hubungi-kami';
                    } else {
                        currentSectionId = lastSection.getAttribute('id');
                    }
                }
            } else if (!foundCurrent && pageYOffset < (sections[0]?.offsetTop - scrollBuffer || 0)) {
                currentSectionId = 'home'; // If scrolled to top before first section
            }


            desktopNavLinks.forEach(link => {
                link.classList.remove('active-nav-link');
                if (link.getAttribute('href') === `#${currentSectionId}`) {
                    link.classList.add('active-nav-link');
                }
            });
            mobileNavLinks.forEach(link => {
                link.classList.remove('active-nav-link');
                if (link.getAttribute('href') === `#${currentSectionId}`) {
                    link.classList.add('active-nav-link');
                }
            });

            if (backToTopBtn) {
                if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
                    backToTopBtn.style.display = "flex";
                } else {
                    backToTopBtn.style.display = "none";
                }
            }
        }, 100);
    }

    window.addEventListener('scroll', updateActiveNavLinkOnScroll);
    updateActiveNavLinkOnScroll(); // Initial check

    if (backToTopBtn) {
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }
}); 