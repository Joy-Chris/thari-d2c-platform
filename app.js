/**
 * Thari Handloom D2C Platform - Frontend Client Application
 */

const ThariApp = (function() {
  // Cart state persisted in localStorage
  let cart = JSON.parse(localStorage.getItem('thari_cart') || '[]');
  let currentProductModal = null;

  function init() {
    updateCartBadge();
    bindGlobalEvents();
  }

  function bindGlobalEvents() {
    // Cart open/close triggers
    document.querySelectorAll('[data-action="open-cart"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openCartDrawer();
      });
    });

    const closeCartBtn = document.getElementById('closeCartBtn');
    if (closeCartBtn) {
      closeCartBtn.addEventListener('click', closeCartDrawer);
    }

    const cartBackdrop = document.getElementById('cartDrawerBackdrop');
    if (cartBackdrop) {
      cartBackdrop.addEventListener('click', (e) => {
        if (e.target === cartBackdrop) closeCartDrawer();
      });
    }

    // Modal close triggers
    document.querySelectorAll('.modal-close-btn, .modal-backdrop').forEach(el => {
      el.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-backdrop') || e.target.closest('.modal-close-btn')) {
          closeAllModals();
        }
      });
    });

    // Escape key closes modals/drawer
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeAllModals();
        closeCartDrawer();
      }
    });
  }

  // Toast Notification
  function showToast(message, title = 'Thari Notification') {
    const container = document.getElementById('toastContainer') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <div style="flex: 1;">
        <div style="font-weight: 700; font-size: 0.85rem; color: #E8CF82;">${title}</div>
        <div>${message}</div>
      </div>
      <button style="background: none; border: none; color: #fff; cursor: pointer; font-size: 1.1rem;" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4500);
  }

  function createToastContainer() {
    const c = document.createElement('div');
    c.id = 'toastContainer';
    c.className = 'toast-container';
    document.body.appendChild(c);
    return c;
  }

  // Cart Management
  function addToCart(product, quantity = 1) {
    const existing = cart.find(item => item.product_id === product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      cart.push({
        product_id: product.id,
        title: product.title,
        price_inr: product.price_inr,
        craft_tradition: product.craft_tradition,
        artisan_id: product.artisan_id,
        artisan_name: product.artisan ? product.artisan.full_name : 'Master Weaver',
        artisan_share_pct: product.artisan ? (product.artisan.fair_trade_share_percent || 82) : 82,
        image: (product.images && product.images.length > 0) ? product.images[0] : 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=400&q=80',
        quantity: quantity
      });
    }
    saveCart();
    updateCartBadge();
    showToast(`"${product.title.substring(0, 32)}..." added to cart!`, 'Handloom Cart Updated');
    renderCartDrawerItems();
  }

  function removeFromCart(productId) {
    cart = cart.filter(item => item.product_id !== productId);
    saveCart();
    updateCartBadge();
    renderCartDrawerItems();
  }

  function updateQuantity(productId, delta) {
    const item = cart.find(i => i.product_id === productId);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity <= 0) {
      removeFromCart(productId);
    } else {
      saveCart();
      updateCartBadge();
      renderCartDrawerItems();
    }
  }

  function saveCart() {
    localStorage.setItem('thari_cart', JSON.stringify(cart));
  }

  function updateCartBadge() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.querySelectorAll('.cart-badge-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'inline-flex' : 'none';
    });
  }

  function openCartDrawer() {
    renderCartDrawerItems();
    const drawer = document.getElementById('cartDrawerBackdrop');
    if (drawer) drawer.classList.add('open');
  }

  function closeCartDrawer() {
    const drawer = document.getElementById('cartDrawerBackdrop');
    if (drawer) drawer.classList.remove('open');
  }

  function renderCartDrawerItems() {
    const container = document.getElementById('cartItemsList');
    const totalEl = document.getElementById('cartDrawerTotal');
    const artisanPayoutEl = document.getElementById('cartDrawerArtisanPayout');
    const checkoutBtn = document.getElementById('cartCheckoutBtn');
    if (!container) return;

    if (cart.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--color-text-muted);">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🧵</div>
          <h4 style="font-family: var(--font-serif); color: var(--color-indigo); margin-bottom: 0.5rem;">Your loom basket is empty</h4>
          <p style="font-size: 0.88rem;">Explore heritage weaves crafted by India's master artisans.</p>
        </div>
      `;
      if (totalEl) totalEl.textContent = '₹0';
      if (artisanPayoutEl) artisanPayoutEl.textContent = '₹0';
      if (checkoutBtn) checkoutBtn.disabled = true;
      return;
    }

    let total = 0;
    let totalArtisanPayout = 0;

    let html = '';
    cart.forEach(item => {
      const lineTotal = item.price_inr * item.quantity;
      const lineArtisan = Math.round(lineTotal * (item.artisan_share_pct / 100));
      total += lineTotal;
      totalArtisanPayout += lineArtisan;

      html += `
        <div style="display: flex; gap: 0.85rem; padding: 0.85rem 0; border-bottom: 1px solid var(--color-silk-border);">
          <img src="${item.image}" alt="${item.title}" style="width: 65px; height: 65px; border-radius: var(--radius-sm); object-fit: cover;">
          <div style="flex: 1;">
            <div style="font-size: 0.85rem; font-weight: 600; line-height: 1.3; color: var(--color-indigo);">${item.title}</div>
            <div style="font-size: 0.76rem; color: var(--color-text-muted); margin-top: 2px;">Weaver: ${item.artisan_name}</div>
            <div style="font-size: 0.76rem; color: var(--color-temple-green); font-weight: 600;">₹${lineArtisan.toLocaleString('en-IN')} direct to weaver</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 0.5rem;">
              <div style="display: flex; align-items: center; gap: 0.4rem; background: var(--color-silk-bg); border-radius: 4px; padding: 2px 6px; border: 1px solid var(--color-silk-border);">
                <button onclick="ThariApp.updateQuantity('${item.product_id}', -1)" style="border: none; background: none; cursor: pointer; font-weight: bold; width: 18px;">-</button>
                <span style="font-size: 0.82rem; font-weight: 600;">${item.quantity}</span>
                <button onclick="ThariApp.updateQuantity('${item.product_id}', 1)" style="border: none; background: none; cursor: pointer; font-weight: bold; width: 18px;">+</button>
              </div>
              <div style="font-weight: 700; color: var(--color-indigo);">₹${lineTotal.toLocaleString('en-IN')}</div>
            </div>
          </div>
          <button onclick="ThariApp.removeFromCart('${item.product_id}')" title="Remove" style="background: none; border: none; color: #C85E46; cursor: pointer; font-size: 1.1rem; align-self: flex-start;">&times;</button>
        </div>
      `;
    });

    container.innerHTML = html;
    if (totalEl) totalEl.textContent = `₹${total.toLocaleString('en-IN')}`;
    if (artisanPayoutEl) artisanPayoutEl.textContent = `₹${totalArtisanPayout.toLocaleString('en-IN')}`;
    if (checkoutBtn) checkoutBtn.disabled = false;
  }

  // Product Detail Modal
  async function openProductModal(productId) {
    try {
      const resp = await fetch(`/api/v1/products/${productId}`);
      if (!resp.ok) throw new Error('Product not found');
      const prod = await resp.json();
      currentProductModal = prod;

      const modalContent = document.getElementById('productModalContent');
      if (!modalContent) return;

      const pricing = prod.transparent_pricing || {
        artisan_wages: Math.round(prod.price_inr * 0.82),
        raw_material_silk_zari: Math.round(prod.price_inr * 0.12),
        finishing_packaging: 250,
        platform_fair_trade_ops: Math.round(prod.price_inr * 0.05)
      };

      const artisanSharePct = Math.round((pricing.artisan_wages / prod.price_inr) * 100);

      modalContent.innerHTML = `
        <div style="display: grid; grid-template-columns: 1fr 1.1fr; gap: 2rem; padding: 2rem;" class="modal-grid-wrap">
          <div>
            <img id="modalMainImg" src="${prod.images[0] || 'https://images.unsplash.com/photo-1610030469983-98e550d6193c'}" alt="${prod.title}" style="width: 100%; border-radius: var(--radius-md); aspect-ratio: 4/3; object-fit: cover; box-shadow: var(--shadow-sm);">
            ${prod.images.length > 1 ? `
              <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                ${prod.images.map((img, idx) => `
                  <img src="${img}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px; cursor: pointer; border: 2px solid ${idx===0 ? 'var(--color-terracotta)' : 'transparent'};" onclick="document.getElementById('modalMainImg').src='${img}'">
                `).join('')}
              </div>
            ` : ''}
            
            <!-- Artisan Story Card -->
            ${prod.artisan ? `
              <div style="background: var(--color-silk-bg); border: 1px solid var(--color-silk-border); border-radius: var(--radius-md); padding: 1.25rem; margin-top: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                  <img src="${prod.artisan.avatar_url}" alt="${prod.artisan.full_name}" style="width: 46px; height: 46px; border-radius: 50%; object-fit: cover;">
                  <div>
                    <div style="font-weight: 700; color: var(--color-indigo);">${prod.artisan.full_name}</div>
                    <div style="font-size: 0.78rem; color: var(--color-text-muted);">${prod.artisan.cluster_name} (${prod.artisan.state})</div>
                  </div>
                </div>
                <div style="display: flex; gap: 0.4rem; flex-wrap: wrap; margin-bottom: 0.75rem;">
                  ${(prod.artisan.certifications || []).map(c => `<span class="badge-gi" style="font-size: 0.68rem;">✓ ${c}</span>`).join('')}
                </div>
                <button class="btn btn-secondary btn-sm" style="width: 100%;" onclick="ThariApp.openInquiryModal('${prod.id}', '${prod.artisan_id}', '${prod.artisan.full_name}')">
                  💬 Direct Message / Custom Query
                </button>
              </div>
            ` : ''}
          </div>

          <div>
            <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap;">
              <span class="badge-fairshare">♥ ${artisanSharePct}% Direct Weaver Share</span>
              ${prod.gi_tag_certified ? `<span class="badge-gi">🏛 GI Certified Origin</span>` : ''}
              ${prod.handloom_mark ? `<span class="badge-craftmark">🌿 Handloom Mark</span>` : ''}
            </div>

            <h2 style="font-size: 1.65rem; line-height: 1.25; margin-bottom: 0.75rem;">${prod.title}</h2>
            <div style="font-size: 0.85rem; color: var(--color-terracotta); font-weight: 700; text-transform: uppercase; margin-bottom: 1rem;">
              ${prod.craft_tradition} • ${prod.origin_cluster || 'India'}
            </div>

            <div style="display: flex; align-items: baseline; gap: 1rem; margin-bottom: 1.25rem;">
              <span style="font-family: var(--font-serif); font-size: 2rem; font-weight: 700; color: var(--color-indigo);">
                ₹${prod.price_inr.toLocaleString('en-IN')}
              </span>
              <span style="font-size: 0.88rem; color: var(--color-temple-green); font-weight: 600;">
                (₹${pricing.artisan_wages.toLocaleString('en-IN')} paid directly to weaver)
              </span>
            </div>

            <p style="font-size: 0.92rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem;">
              ${prod.detailed_story}
            </p>

            <!-- Technical Handloom Specifications -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; background: var(--color-silk-bg); padding: 1rem; border-radius: var(--radius-md); font-size: 0.82rem; margin-bottom: 1.5rem; border: 1px solid var(--color-silk-border);">
              <div><strong style="color: var(--color-indigo);">Loom Time:</strong> ${prod.loom_days} days on loom</div>
              <div><strong style="color: var(--color-indigo);">Material:</strong> ${prod.material}</div>
              <div><strong style="color: var(--color-indigo);">Warp Yarn:</strong> ${prod.warp_yarn || 'Pure Silk 20/22D'}</div>
              <div><strong style="color: var(--color-indigo);">Weft Yarn:</strong> ${prod.weft_yarn || 'Cotton 100s'}</div>
              <div><strong style="color: var(--color-indigo);">Dye Method:</strong> ${prod.dye_type || 'Natural/Eco Dyes'}</div>
              <div><strong style="color: var(--color-indigo);">Dimensions:</strong> ${prod.dimensions}</div>
            </div>

            <!-- Transparent Handloom Economics -->
            <div class="pricing-breakdown-box">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 0.85rem; color: var(--color-indigo);">Transparent Fair-Trade Cost Breakdown</strong>
                <span style="font-size: 0.75rem; color: var(--color-text-muted);">Zero Middlemen Cut</span>
              </div>
              <div class="breakdown-bar">
                <div class="bar-segment-wages" style="width: ${(pricing.artisan_wages/prod.price_inr)*100}%;" title="Weaver Fair Wages"></div>
                <div class="bar-segment-material" style="width: ${(pricing.raw_material_silk_zari/prod.price_inr)*100}%;" title="Yarn & Zari"></div>
                <div class="bar-segment-finishing" style="width: ${(pricing.finishing_packaging/prod.price_inr)*100}%;" title="Artisanal Finishing"></div>
                <div class="bar-segment-ops" style="width: ${(pricing.platform_fair_trade_ops/prod.price_inr)*100}%;" title="Platform Operations"></div>
              </div>
              <div class="breakdown-legend">
                <div class="legend-item"><span class="legend-dot" style="background:#2B4C3F;"></span> Weaver Wages: ₹${pricing.artisan_wages.toLocaleString('en-IN')}</div>
                <div class="legend-item"><span class="legend-dot" style="background:#C97D1A;"></span> Silk/Cotton/Zari: ₹${pricing.raw_material_silk_zari.toLocaleString('en-IN')}</div>
                <div class="legend-item"><span class="legend-dot" style="background:#325875;"></span> Packaging: ₹${pricing.finishing_packaging.toLocaleString('en-IN')}</div>
                <div class="legend-item"><span class="legend-dot" style="background:#A8422B;"></span> Ops & Escrow: ₹${pricing.platform_fair_trade_ops.toLocaleString('en-IN')}</div>
              </div>
            </div>

            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
              <button class="btn btn-primary" style="flex: 1;" onclick="ThariApp.addToCart(ThariApp.getCurrentProduct(), 1); ThariApp.closeAllModals();">
                🛍 Add to Loom Basket
              </button>
              <button class="btn btn-indigo" onclick="ThariApp.addToCart(ThariApp.getCurrentProduct(), 1); ThariApp.closeAllModals(); ThariApp.openCartDrawer();">
                ⚡ Direct Buy
              </button>
            </div>

            <!-- Customer Reviews Section -->
            <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--color-silk-border);">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="font-family: var(--font-serif); font-size: 1.1rem; color: var(--color-indigo);">Conscious Patron Reviews (${prod.reviews ? prod.reviews.length : 0})</h4>
                <button class="btn btn-secondary btn-sm" onclick="ThariApp.toggleReviewForm()">+ Write Review</button>
              </div>

              <!-- Inline Review Form -->
              <div id="inlineReviewForm" style="display: none; background: var(--color-silk-bg); padding: 1rem; border-radius: var(--radius-md); margin-bottom: 1rem; border: 1px solid var(--color-silk-border);">
                <div class="form-group">
                  <label class="form-label">Your Name</label>
                  <input type="text" id="reviewCustomerName" class="form-control" placeholder="e.g. Sumanth Patel">
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Rating</label>
                    <select id="reviewRating" class="form-control">
                      <option value="5">★★★★★ (5/5 Exceptional Craft)</option>
                      <option value="4">★★★★☆ (4/5 Very Good)</option>
                      <option value="3">★★★☆☆ (3/5 Good)</option>
                    </select>
                  </div>
                </div>
                <div class="form-group">
                  <label class="form-label">Craft & Weave Feedback</label>
                  <textarea id="reviewComment" class="form-control" rows="2" placeholder="Describe the tactile feel, drape, and artisan appreciation..."></textarea>
                </div>
                <button class="btn btn-primary btn-sm" onclick="ThariApp.submitReview('${prod.id}')">Submit Patron Review</button>
              </div>

              <div id="modalReviewsList">
                ${(prod.reviews && prod.reviews.length > 0) ? prod.reviews.map(r => `
                  <div style="padding: 0.75rem 0; border-bottom: 1px solid var(--color-silk-border);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                      <strong style="font-size: 0.85rem; color: var(--color-indigo);">${r.customer_name}</strong>
                      <span style="color: var(--color-gold); font-size: 0.82rem;">${'★'.repeat(r.rating)}</span>
                    </div>
                    <p style="font-size: 0.82rem; color: var(--color-text-muted); margin-top: 0.25rem;">"${r.comment}"</p>
                  </div>
                `).join('') : '<p style="font-size: 0.82rem; color: var(--color-text-muted);">Be the first conscious patron to review this handloom piece.</p>'}
              </div>
            </div>
          </div>
        </div>
      `;

      const modal = document.getElementById('productDetailModal');
      if (modal) modal.classList.add('open');
    } catch (err) {
      console.error(err);
      showToast('Could not load handloom details.', 'Error');
    }
  }

  function getCurrentProduct() {
    return currentProductModal;
  }

  function toggleReviewForm() {
    const f = document.getElementById('inlineReviewForm');
    if (f) f.style.display = f.style.display === 'none' ? 'block' : 'none';
  }

  async function submitReview(productId) {
    const name = document.getElementById('reviewCustomerName').value.trim();
    const rating = parseInt(document.getElementById('reviewRating').value);
    const comment = document.getElementById('reviewComment').value.trim();

    if (!name || !comment) {
      alert('Please fill out your name and comments.');
      return;
    }

    try {
      const resp = await fetch(`/api/v1/products/${productId}/reviews`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_name: name,
          rating: rating,
          comment: comment
        })
      });
      if (!resp.ok) throw new Error('Failed to submit review');
      showToast('Thank you! Your artisan appreciation review has been posted.', 'Review Added');
      openProductModal(productId);
    } catch (err) {
      alert(err.message);
    }
  }

  // Direct Weaver Inquiry Modal
  function openInquiryModal(productId, artisanId, artisanName) {
    const modal = document.getElementById('inquiryModal');
    if (!modal) return;
    document.getElementById('inquiryArtisanId').value = artisanId;
    document.getElementById('inquiryProductId').value = productId || '';
    document.getElementById('inquiryArtisanTitle').textContent = `Direct Message to ${artisanName}`;
    modal.classList.add('open');
  }

  async function submitInquiry(e) {
    e.preventDefault();
    const artisanId = document.getElementById('inquiryArtisanId').value;
    const productId = document.getElementById('inquiryProductId').value || null;
    const name = document.getElementById('inquiryCustomerName').value;
    const email = document.getElementById('inquiryCustomerEmail').value;
    const phone = document.getElementById('inquiryCustomerPhone').value;
    const message = document.getElementById('inquiryMessage').value;
    const dimensions = document.getElementById('inquiryDimensions').value;

    try {
      const resp = await fetch('/api/v1/inquiries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          artisan_id: artisanId,
          product_id: productId,
          customer_name: name,
          customer_email: email,
          customer_phone: phone,
          message: message,
          custom_dimensions_requested: dimensions || null
        })
      });
      if (!resp.ok) throw new Error('Could not deliver inquiry');
      closeAllModals();
      showToast('Your message has been sent directly to the artisan cooperative!', 'Weaver Contacted');
    } catch (err) {
      alert(err.message);
    }
  }

  // Checkout Modal
  function openCheckoutModal() {
    if (cart.length === 0) return;
    closeCartDrawer();
    const modal = document.getElementById('checkoutModal');
    if (!modal) return;

    let subtotal = 0;
    let artisanPayout = 0;
    cart.forEach(item => {
      const line = item.price_inr * item.quantity;
      subtotal += line;
      artisanPayout += Math.round(line * (item.artisan_share_pct / 100));
    });

    document.getElementById('checkoutSubtotal').textContent = `₹${subtotal.toLocaleString('en-IN')}`;
    document.getElementById('checkoutArtisanPayout').textContent = `₹${artisanPayout.toLocaleString('en-IN')}`;
    modal.classList.add('open');
  }

  async function submitOrder(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('placeOrderBtn');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Securing Escrow with Weavers...';
    }

    const payload = {
      customer_name: document.getElementById('orderName').value.trim(),
      customer_email: document.getElementById('orderEmail').value.trim(),
      customer_phone: document.getElementById('orderPhone').value.trim(),
      shipping_address: {
        street: document.getElementById('orderStreet').value.trim(),
        city: document.getElementById('orderCity').value.trim(),
        state: document.getElementById('orderState').value.trim(),
        pincode: document.getElementById('orderPincode').value.trim(),
        country: 'India'
      },
      items: cart.map(i => ({ product_id: i.product_id, quantity: i.quantity })),
      payment_method: document.getElementById('orderPaymentMethod').value
    };

    try {
      const resp = await fetch('/api/v1/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) {
        const errorData = await resp.json();
        throw new Error(errorData.detail || 'Order placement failed');
      }
      const order = await resp.json();

      // Clear cart
      cart = [];
      saveCart();
      updateCartBadge();
      closeAllModals();

      // Show Order Success Modal
      showOrderSuccess(order);
    } catch (err) {
      alert(err.message);
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Confirm Order & Pay Weavers';
      }
    }
  }

  function showOrderSuccess(order) {
    const modal = document.getElementById('orderSuccessModal');
    if (!modal) return;
    document.getElementById('successOrderId').textContent = order.order_id;
    document.getElementById('successTracking').textContent = order.tracking_number;
    document.getElementById('successAmount').textContent = `₹${order.total_inr.toLocaleString('en-IN')}`;
    document.getElementById('successArtisanPayout').textContent = `₹${order.total_artisan_direct_payout_inr.toLocaleString('en-IN')}`;
    modal.classList.add('open');
  }

  function closeAllModals() {
    document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('open'));
  }

  return {
    init,
    addToCart,
    removeFromCart,
    updateQuantity,
    openCartDrawer,
    closeCartDrawer,
    openProductModal,
    getCurrentProduct,
    toggleReviewForm,
    submitReview,
    openInquiryModal,
    submitInquiry,
    openCheckoutModal,
    submitOrder,
    closeAllModals,
    showToast
  };
})();

document.addEventListener('DOMContentLoaded', ThariApp.init);
