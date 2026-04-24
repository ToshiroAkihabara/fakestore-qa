import React, { useEffect, useState } from 'react';

const API = import.meta.env.VITE_API_BASE_URL || 'https://fakestoreapi.com';
const HOME_HASH = '#/';
const LOGIN_HASH = '#/login';
const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
});

function parseRoute(hashValue) {
  if (hashValue === LOGIN_HASH) {
    return { page: 'login' };
  }

  const productMatch = hashValue.match(/^#\/product\/(\d+)$/);
  if (productMatch) {
    return { page: 'product', productId: Number(productMatch[1]) };
  }

  return { page: 'home' };
}

function navigateTo(hashValue) {
  window.location.hash = hashValue;
}

function ProductCard({ product, onAddToCart, onViewProduct }) {
  return (
    <article className="product-card" data-testid="product-card">
      <div className="product-card__media">
        <img
          alt={product.title}
          className="product-card__image"
          src={product.image}
        />
      </div>
      <div className="product-card__body">
        <p className="product-card__category">{product.category}</p>
        <h2 className="product-card__title">{product.title}</h2>
        <p className="product-card__price">
          {currencyFormatter.format(product.price)}
        </p>
      </div>
      <div className="product-card__actions">
        <button
          data-testid="add-to-cart-button"
          onClick={() => onAddToCart(product)}
          type="button"
        >
          Add to Cart
        </button>
        <button
          className="button-secondary"
          data-testid="view-product-button"
          onClick={() => onViewProduct(product.id)}
          type="button"
        >
          View
        </button>
      </div>
    </article>
  );
}

function LoginPanel({ errorMessage, isSubmitting, onSubmit }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  async function handleSubmit(event) {
    event.preventDefault();
    await onSubmit(username, password);
  }

  return (
    <section className="panel panel--narrow">
      <div className="eyebrow">Account access</div>
      <h1 className="panel__title">Log in to continue testing the store</h1>
      <p className="panel__copy">
        Use the public Fake Store test account to verify the login path.
      </p>
      <form className="login-form" data-testid="login-form" onSubmit={handleSubmit}>
        <label className="field">
          <span>Username</span>
          <input
            data-testid="login-username"
            onChange={(event) => setUsername(event.target.value)}
            placeholder="mor_2314"
            value={username}
          />
        </label>
        <label className="field">
          <span>Password</span>
          <input
            data-testid="login-password"
            onChange={(event) => setPassword(event.target.value)}
            placeholder="83r5^_"
            type="password"
            value={password}
          />
        </label>
        <button data-testid="login-submit" disabled={isSubmitting} type="submit">
          {isSubmitting ? 'Signing in...' : 'Login'}
        </button>
        {errorMessage ? (
          <p className="feedback feedback--error" data-testid="login-error">
            {errorMessage}
          </p>
        ) : null}
      </form>
    </section>
  );
}

function ProductDetail({ product, onAddToCart, onBack }) {
  if (!product) {
    return (
      <section className="panel">
        <h1 className="panel__title">Product not found</h1>
        <p className="panel__copy">
          The selected product could not be matched to the current catalogue.
        </p>
        <button onClick={onBack} type="button">
          Return to home
        </button>
      </section>
    );
  }

  return (
    <section className="product-detail panel" data-testid="product-detail">
      <div className="product-detail__image-wrap">
        <img
          alt={product.title}
          className="product-detail__image"
          src={product.image}
        />
      </div>
      <div className="product-detail__content">
        <p className="eyebrow">{product.category}</p>
        <h1 className="panel__title" data-testid="product-title">
          {product.title}
        </h1>
        <p className="product-detail__price" data-testid="product-price">
          {currencyFormatter.format(product.price)}
        </p>
        <p className="panel__copy">{product.description}</p>
        <div className="product-detail__actions">
          <button data-testid="add-to-cart-button" onClick={() => onAddToCart(product)} type="button">
            Add to Cart
          </button>
          <button className="button-secondary" onClick={onBack} type="button">
            Back to catalogue
          </button>
        </div>
      </div>
    </section>
  );
}

function Navigation({ cartCount, onHome, onLogin, onLogout, user }) {
  return (
    <header className="app-header">
      <div className="brand-block">
        <p className="eyebrow">QA portfolio</p>
        <h1 className="brand-block__title">Fake Storefront</h1>
      </div>
      <nav className="nav-actions">
        <button data-testid="nav-home" onClick={onHome} type="button">
          Home
        </button>
        {user ? (
          <button data-testid="logout-button" onClick={onLogout} type="button">
            Logout ({user.username})
          </button>
        ) : (
          <button className="button-secondary" data-testid="nav-login" onClick={onLogin} type="button">
            Login
          </button>
        )}
        <div aria-label={`Cart contains ${cartCount} items`} className="cart-pill">
          <span className="cart-pill__label">Cart</span>
          <span data-testid="cart-count">{cartCount}</span>
        </div>
      </nav>
    </header>
  );
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [productsLoading, setProductsLoading] = useState(true);
  const [productsError, setProductsError] = useState('');
  const [cart, setCart] = useState([]);
  const [route, setRoute] = useState(() => parseRoute(window.location.hash));
  const [user, setUser] = useState(null);
  const [loginError, setLoginError] = useState('');
  const [loginSuccess, setLoginSuccess] = useState('');
  const [isSubmittingLogin, setIsSubmittingLogin] = useState(false);

  useEffect(() => {
    if (!window.location.hash) {
      window.history.replaceState(null, '', HOME_HASH);
    }

    function syncRoute() {
      setRoute(parseRoute(window.location.hash));
    }

    syncRoute();
    window.addEventListener('hashchange', syncRoute);
    return () => window.removeEventListener('hashchange', syncRoute);
  }, []);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    async function loadProducts() {
      setProductsLoading(true);
      setProductsError('');

      try {
        const response = await fetch(`${API}/products`, { signal: controller.signal });
        if (!response.ok) {
          throw new Error(`Unexpected status ${response.status}`);
        }

        const data = await response.json();
        if (isMounted) {
          setProducts(data);
        }
      } catch (error) {
        if (controller.signal.aborted) {
          return;
        }

        if (isMounted) {
          setProductsError('We could not load the catalogue right now.');
        }
      } finally {
        if (isMounted) {
          setProductsLoading(false);
        }
      }
    }

    loadProducts();
    return () => {
      isMounted = false;
      controller.abort();
    };
  }, []);

  const selectedProduct =
    route.page === 'product'
      ? products.find((product) => product.id === route.productId) || null
      : null;

  function addToCart(product) {
    setCart((currentCart) => [...currentCart, product]);
  }

  async function handleLogin(username, password) {
    setIsSubmittingLogin(true);
    setLoginError('');

    try {
      const response = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      setUser({ username, token: data.token });
      setLoginSuccess(`Logged in as ${username}`);
      navigateTo(HOME_HASH);
    } catch (error) {
      setLoginError('Invalid username or password');
    } finally {
      setIsSubmittingLogin(false);
    }
  }

  function handleLogout() {
    setUser(null);
    setLoginSuccess('');
    setLoginError('');
    navigateTo(HOME_HASH);
  }

  function renderBody() {
    if (route.page === 'login') {
      return (
        <LoginPanel
          errorMessage={loginError}
          isSubmitting={isSubmittingLogin}
          onSubmit={handleLogin}
        />
      );
    }

    if (route.page === 'product') {
      if (productsLoading) {
        return (
          <section className="panel status-panel" data-testid="products-loading">
            Loading products...
          </section>
        );
      }

      if (productsError) {
        return (
          <section className="feedback feedback--error" data-testid="products-error">
            {productsError}
          </section>
        );
      }

      return (
        <ProductDetail
          onAddToCart={addToCart}
          onBack={() => navigateTo(HOME_HASH)}
          product={selectedProduct}
        />
      );
    }

    return (
      <>
        <section className="hero panel">
          <div>
            <p className="eyebrow">Automation playground</p>
            <h2 className="panel__title">A compact storefront built for API and UI coverage</h2>
            <p className="panel__copy">
              Browse products from Fake Store API, inspect details, add items to a local cart,
              and validate authentication flows with predictable selectors.
            </p>
          </div>
          <div className="hero__stats">
            <div>
              <span className="hero__stat-label">Products loaded</span>
              <strong>{products.length}</strong>
            </div>
            <div>
              <span className="hero__stat-label">Cart items</span>
              <strong>{cart.length}</strong>
            </div>
          </div>
        </section>

        {loginSuccess ? (
          <section className="feedback feedback--success" data-testid="login-success">
            {loginSuccess}
          </section>
        ) : null}

        {productsLoading ? (
          <section className="panel status-panel" data-testid="products-loading">
            Loading products...
          </section>
        ) : null}

        {productsError ? (
          <section className="feedback feedback--error" data-testid="products-error">
            {productsError}
          </section>
        ) : null}

        {!productsLoading && !productsError ? (
          <section className="product-grid">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                onAddToCart={addToCart}
                onViewProduct={(productId) => navigateTo(`#/product/${productId}`)}
                product={product}
              />
            ))}
          </section>
        ) : null}
      </>
    );
  }

  return (
    <div className="app-shell" data-testid="page-root">
      <Navigation
        cartCount={cart.length}
        onHome={() => navigateTo(HOME_HASH)}
        onLogin={() => navigateTo(LOGIN_HASH)}
        onLogout={handleLogout}
        user={user}
      />
      <main className="content-shell">{renderBody()}</main>
    </div>
  );
}
