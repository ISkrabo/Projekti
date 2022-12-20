using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Tobii.G2OM;

public class TargetFocusHighlight : MonoBehaviour, IGazeFocusable
{
    
    private static readonly int _baseColor = Shader.PropertyToID("_BaseColor");
    private Color _originalColor = Color.white;
    public Color highlightColor = Color.red;
    private Color _targetColor;
    private Renderer _renderer;
    public float animationTime = 0.1f;
    
    public void GazeFocusChanged(bool hasFocus)
        {
            //If this object received focus, fade the object's color to highlight color
            if (hasFocus)
            {
                _targetColor = highlightColor;
            }
            //If this object lost focus, fade the object's color to it's original color
            else
            {
                _targetColor = _originalColor;
            }
        }

    // Start is called before the first frame update
    void Start()
    {
        _renderer = GetComponent<Renderer>();
        _renderer.material.color = _originalColor;
        _targetColor = _originalColor;
    }

    // Update is called once per frame
    void Update()
    {
        if (_renderer.material.HasProperty(_baseColor)) // new rendering pipeline (lightweight, hd, universal...)
        {
            _renderer.material.SetColor(_baseColor, Color.Lerp(_renderer.material.GetColor(_baseColor), _targetColor, Time.deltaTime * (1 / animationTime)));
        }
        else // old standard rendering pipline
        {
            _renderer.material.color = Color.Lerp(_renderer.material.color, _targetColor, Time.deltaTime * (1 / animationTime));
        }
    }
}
