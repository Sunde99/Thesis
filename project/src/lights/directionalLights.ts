import * as THREE from 'three'

export const createDirectionalLights = (scene: THREE.Scene) => {
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.castShadow = true
  directionalLight.position.set(-65, 30, -65)

  const directionalLightHelper = new THREE.DirectionalLightHelper(
    directionalLight,
    5,
    0xff000f,
  )
  // directionalLightHelper.matrixAutoUpdate = true

  scene.add(directionalLight)
  scene.add(directionalLightHelper)
  return directionalLight
}
