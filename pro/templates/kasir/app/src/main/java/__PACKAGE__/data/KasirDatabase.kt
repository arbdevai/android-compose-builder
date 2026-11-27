package __PACKAGE__.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [Product::class, Sale::class, SaleItem::class],
    version = 1,
    exportSchema = false
)
abstract class KasirDatabase : RoomDatabase() {
    abstract fun kasirDao(): KasirDao

    companion object {
        @Volatile
        private var instance: KasirDatabase? = null

        fun getInstance(context: Context): KasirDatabase {
            return instance ?: synchronized(this) {
                instance ?: Room.databaseBuilder(
                    context.applicationContext,
                    KasirDatabase::class.java,
                    "kasir.db"
                ).build().also { instance = it }
            }
        }
    }
}
