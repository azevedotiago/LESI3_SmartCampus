package ipca.example.smartenergy

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView

class DeviceDetailActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_device_detail)
/*
        val iddevices = intent.getStringExtra("iddevices")
        val macaddress = intent.getStringExtra("macaddress")
        println("#### DeviceDetailActivity | iddevices: $iddevices")

        findViewById<TextView>(R.id.textViewTitle).text = iddevices
        findViewById<TextView>(R.id.textViewDetail).text = macaddress */
    }
}