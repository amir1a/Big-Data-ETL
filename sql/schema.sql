CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(255) NOT NULL, 
    img_url VARCHAR(255),
    product_url VARCHAR(255),
    stars DECIMAL(2,1),
    reviews INTEGER,
    price DECIMAL(10,2),
    list_price DECIMAL(10,2),
    category_id INTEGER REFERENCES categories(category_id),
    is_best_seller BOOLEAN,
    bought_in_last_month INTEGER,
    price_category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id VARCHAR(20) REFERENCES products(product_id),
    rating DECIMAL(2,1),
    review_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_products_category_id ON products (category_id);
CREATE INDEX idx_reviews_product_id ON reviews (product_id);