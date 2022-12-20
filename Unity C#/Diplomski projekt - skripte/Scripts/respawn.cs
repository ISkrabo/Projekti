using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class respawn : MonoBehaviour
{

    private Vector3 startpos;
    private Quaternion startrot;
    // Start is called before the first frame update
    void Start()
    {
        startpos = this.transform.position;
        startrot = this.transform.rotation;
    }

    // Update is called once per frame
    void Update()
    {
        if (this.transform.position.y < -0.29) {
            this.GetComponent<Rigidbody>().isKinematic = true;
            this.GetComponent<Rigidbody>().isKinematic = false;
            this.transform.position = startpos;
            this.transform.rotation = startrot;
        }
    }
}
