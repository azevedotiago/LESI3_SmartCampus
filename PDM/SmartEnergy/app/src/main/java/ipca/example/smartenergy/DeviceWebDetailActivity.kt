package ipca.example.smartenergy

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.webkit.WebView
import org.json.JSONObject

class DeviceWebDetailActivity : AppCompatActivity() {

    var device : Device? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_device_web_detail)
        device = Device.fromJSON(JSONObject(intent.getStringExtra(MainActivity.EXTRA_ARTICLE).toString()))
        println("#### DeviceWebDetailActivity | device: "+device?.iddevices)
        title = device?.iddevices + " - " + device?.detail + " ("+ device?.macaddress + ")"
        device?.status?.let {
            findViewById<WebView>(R.id.webView).loadUrl(it)
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_device,menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when(item.itemId){
            R.id.action_share -> {
                val intent = Intent(Intent.ACTION_SEND)
                intent.putExtra(Intent.EXTRA_TEXT, device?.coordinatey)
                intent.type = "text/plain"
                val intentChooser = Intent.createChooser(intent, device?.iddevices)
                startActivity(intentChooser)
                return true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}