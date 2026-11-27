package __PACKAGE__.data

import kotlinx.coroutines.flow.Flow

/**
 * Lapisan repository: satu-satunya pintu masuk ViewModel ke database.
 */
class KasirRepository(private val dao: KasirDao) {

    fun observeProducts(): Flow<List<Product>> = dao.observeProducts()

    fun observeSales(): Flow<List<Sale>> = dao.observeSales()

    fun observeTotalRevenue(): Flow<Long> = dao.observeTotalRevenue()

    suspend fun addProduct(name: String, price: Long, stock: Int): Long {
        require(name.isNotBlank()) { "Nama produk tidak boleh kosong" }
        require(price > 0) { "Harga harus lebih dari 0" }
        require(stock >= 0) { "Stok tidak boleh negatif" }
        return dao.insertProduct(Product(name = name.trim(), price = price, stock = stock))
    }

    suspend fun deleteProduct(id: Long): Int = dao.deleteProduct(id)

    suspend fun getSaleItems(saleId: Long): List<SaleItem> = dao.getSaleItems(saleId)

    /**
     * Checkout keranjang (productId -> qty). Mengembalikan id penjualan,
     * atau -1 bila keranjang kosong atau stok tidak mencukupi.
     */
    suspend fun checkout(cart: Map<Long, Int>, products: List<Product>): Long {
        return dao.checkout(cart, products)
    }
}
