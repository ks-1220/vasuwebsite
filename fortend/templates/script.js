// ...existing code...
document.addEventListener('DOMContentLoaded', () => {
  // IntersectionObserver for entrance animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.animate').forEach(el => observer.observe(el));

  // Simple filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = Array.from(document.querySelectorAll('.product-card'));
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      cards.forEach(card => {
        const tags = card.dataset.tags ?? '';
        const match = filter === 'all' || tags.split(',').map(t => t.trim()).includes(filter);
        card.style.display = match ? '' : 'none';
      });
    });
  });

  // Modal logic with keyboard support
  const modal = document.getElementById('product-modal');
  const modalImg = document.getElementById('modal-img');
  const modalTitle = document.getElementById('modal-title');
  const modalPrice = document.getElementById('modal-price');
  const modalDescription = document.getElementById('modal-description');
  const closeModal = () => {
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    lastFocus && lastFocus.focus();
  };

  let lastFocus = null;

  const productsMap = {
    p1: {
      img: 'assets/products/p1.jpg',
      title: 'Classic Leather Wallet',
      price: '$49.00',
      description: 'Hand-stitched wallet, full-grain leather, 6 card slots, coin pocket. Lifetime patina.'
    },
    p2: {
      img: 'assets/products/p2.jpg',
      title: 'Minimalist Backpack',
      price: '$89.00',
      description: 'Water-resistant, padded laptop sleeve, ergonomic straps, ideal for daily commute.'
    },
    p3: {
      img: 'assets/products/p3.jpg',
      title: 'Noise-Cancelling Headphones',
      price: '$199.00',
      description: 'Active noise cancellation, 30h battery, comfortable ear cushions, foldable.'
    }
    // Add more entries for each product (keyed by data-id)
  };

  document.querySelectorAll('.view-details, .product-card').forEach(el => {
    el.addEventListener('click', (e) => {
      const id = e.currentTarget.dataset.id || e.currentTarget.getAttribute('data-id');
      const data = productsMap[id];
      if (!data) return;
      lastFocus = document.activeElement;
      modalImg.src = data.img;
      modalImg.alt = data.title;
      modalTitle.textContent = data.title;
      modalPrice.textContent = data.price;
      modalDescription.textContent = data.description;
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      // focus close button
      modal.querySelector('.modal-close').focus();
    });
  });

  // close handlers
  modal.querySelector('.modal-close').addEventListener('click', closeModal);
  modal.querySelector('.modal-backdrop')?.addEventListener('click', closeModal);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.getAttribute('aria-hidden') === 'false') closeModal();
  });

  // Basic accessible focus trap (small)
  modal.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    const focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
});
// ...existing code...