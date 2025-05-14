# Supabase and GraphQL Integration

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
# Database configuration
DB_USERNAME=username
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=mydatabase
DB_PORT=3306

# JWT Authentication
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
```

## Setting Up Supabase

1. Sign up for a Supabase account at [https://supabase.com/](https://supabase.com/)
2. Create a new project in Supabase
3. Navigate to the project settings to get your:
   - Project URL (SUPABASE_URL)
   - API Key (SUPABASE_KEY) - use the "anon" public key

## Creating Tables in Supabase

Using the Supabase Dashboard, create the following tables:

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Products Table
```sql
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  price INTEGER NOT NULL,
  stock INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Using GraphQL Endpoints

Once your application is running, you can access the GraphQL interface at `/graphql`

### Example Queries

#### Fetch all products
```graphql
query {
  products {
    id
    name
    description
    price
    stock
    created_at
    updated_at
  }
}
```

#### Fetch a specific product
```graphql
query {
  product(id: 1) {
    id
    name
    description
    price
    stock
  }
}
```

### Example Mutations

#### Create a product
```graphql
mutation {
  createProduct(
    product: {
      name: "New Product"
      description: "Product description"
      price: 10000
      stock: 50
    }
  ) {
    id
    name
    description
    price
    stock
  }
}
```

#### Update a product
```graphql
mutation {
  updateProduct(
    id: 1,
    product: {
      name: "Updated Product"
      description: "New description"
      price: 15000
      stock: 75
    }
  ) {
    id
    name
    description
    price
    stock
  }
}
```

#### Delete a product
```graphql
mutation {
  deleteProduct(id: 1)
}
``` 