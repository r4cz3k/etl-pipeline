CREATE TABLE products (
    id int PRIMARY KEY,
    title varchar(255) NOT NULL,
    description text,
    category varchar(255),
    price decimal,
    discountPercentage double precision,
    rating double precision,
    stock int,
    brand varchar(255),
    sku varchar(255),
    weight decimal,
    warrantyInformation varchar(255),
    shippingInformation varchar(255),
    availabilityStatus varchar(255),
    returnPolicy varchar(255),
    minimumOrderQuantity int,
    thumbnail varchar(255),
    dimensions_width double precision,
    dimensions_height double precision,
    dimensions_depth double precision,
    meta_createdAt timestamp,
    meta_updatedAt timestamp,
    meta_barcode varchar(255),
    meta_qrCode varchar(255)
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    product_id int REFERENCES products(id),
    rating double precision NOT NULL,
    comment text,
    date timestamp,
    reviewerName varchar(255),
    reviewerEmail varchar(255)
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    product_id int REFERENCES products(id),
    image_url text
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    product_id int REFERENCES products(id),
    tag text
);