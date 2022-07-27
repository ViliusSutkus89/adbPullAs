package com.viliussutkus89.adb.pull.`as`

import android.graphics.Bitmap
import android.graphics.Canvas
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.doOnLayout
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream

class MainActivity : AppCompatActivity(R.layout.activity_main) {
    override fun onResume() {
        super.onResume()

        val testDir = File(cacheDir, "test")
        window.decorView.rootView.doOnLayout { view ->
            val bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
            view.draw(Canvas(bitmap))
            val screenshotFile = File(testDir, "activityScreenshot.png")
            lifecycleScope.launch(Dispatchers.IO) {
                FileOutputStream(screenshotFile).use { out ->
                    bitmap.compress(Bitmap.CompressFormat.PNG, 50, out)
                }
            }
        }
        lifecycleScope.launch(Dispatchers.IO) {
            val subDirectory = File(testDir, "subDirectory").also { it.mkdirs() }
            for (f in arrayOf("file1.txt", "file2.txt")) {
                FileOutputStream(File(subDirectory, f)).use { out ->
                    out.write("TEST".toByteArray())
                }
            }
        }
    }
}
