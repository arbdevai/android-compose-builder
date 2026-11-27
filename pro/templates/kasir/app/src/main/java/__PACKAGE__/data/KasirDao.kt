package __PACKAGE__.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Transaction
import kotlinx.coroutines.flow.Flow

@Dao
interface KasirDao {

    // Produk
    @Query("SELECT * FROM products ORDER BY name ASC")
    fun observeProducts(): Flow<List<Product>>

    @Query("SELECT * FROM products WHERE id = :id")
    suspend fun getProduct(id: Long): Product?

    @Insert
    suspend fun insertProduct(product: Product): Long

    // Aturan skill: @Query DELETE/UPDATE dengan suspend WAJIB mengembalikan Int.
    @Query("UPDATE products SET stock = stock - :qty WHERE id = :id AND stock >= :qty")
    suspend fun decreaseStock(id: Long, qty: Int): Int

    @Query("UPDATE products SET stock = stock + :qty WHERE id = :id")
    suspend fun increaseStock(id: Long, qty: Int): Int

    @Query("DELETE FROM products WHERE id = :id")
    suspend fun deleteProduct(id: Long): Int

    // Penjualan
    @Insert
    suspend fun insertSale(sale: Sale): Long

    @Insert
    suspend fun insertSaleItems(items: List<SaleItem>)

    @Query("SELECT * FROM sales ORDER BY createdAt DESC")
    fun observeSales(): Flow<List<Sale>>

    @Query("SELECT * FROM sale_items WHERE saleId = :saleId")
    suspend fun getSaleItems(saleId: Long): List<SaleItem>

    @Query("SELECT COALESCE(SUM(total), 0) FROM sales")
    fun observeTotalRevenue(): Flow<Long>

    /**
     * Checkout atomik: kurangi stok, simpan penjualan, simpan item — dalam satu transaksi.
     * Mengembalikan id penjualan, atau -1 jika ada stok yang tidak mencukupi.
     */
    @Transaction
    suspend fun checkout(cart: Map<Long, Int>, products: List<Product>): Long {
        var total = 0L
        val items = mutableListOf<SaleItem>()
        for ((productId, qty) in cart) {
            val product = products.firstOrNull { it.id == productId } ?: return -1
            if (product.stock < qty) return -1
            if (decreaseStock(productId, qty) == 0) return -1
            total += product.price * qty
            items.add(
                SaleItem(
                    saleId = 0,
                    productId = productId,
                    productName = product.name,
                    price = product.price,
                    qty = qty
                )
            )
        }
        if (items.isEmpty()) return -1
        val saleId = insertSale(Sale(total = total, itemCount = items.sumOf { it.qty }))
        insertSaleItems(items.map { it.copy(saleId = saleId) })
        return saleId
    }
}
