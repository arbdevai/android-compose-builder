package __PACKAGE__.data

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Produk yang dijual. Harga disimpan sebagai Long dalam Rupiah (tanpa desimal).
 * Database dimulai kosong — produk ditambahkan pengguna dari layar Produk.
 */
@Entity(tableName = "products")
data class Product(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val price: Long,
    val stock: Int,
    val createdAt: Long = System.currentTimeMillis()
)
