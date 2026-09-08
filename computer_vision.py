"""
Modulo di Computer Vision classica con OpenCV.
Supporta:
- Conversione in scala di grigi e spazio colore HSV
- Riduzione del rumore (Gaussian Blur, Median Blur)
- Rilevamento dei bordi (Canny Edge Detection)
- Binarizzazione e sogliatura (Thresholding di Otsu, Adaptive Thresholding)
- Rilevamento e disegno dei contorni con bounding box
- Filtri colore personalizzati (HSV Color Masking)
- Salvataggio automatico dei risultati elaborati
"""

import os
import sys
import argparse
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:
    print("[!] OpenCV o NumPy non sono ancora installati.")
    print("[*] Esegui: pip install opencv-python numpy")
    sys.exit(1)


class OpenCVVisionPipeline:
    def __init__(self, output_dir: str = "outputs/vision"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_image(self, image_path: str) -> np.ndarray:
        """Carica un'immagine da percorso su disco."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File non trovato: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Impossibile leggere l'immagine (formato non supportato o file corrotto): {image_path}")
        print(f"[+] Immagine caricata con successo: {image_path} ({img.shape[1]}x{img.shape[0]} px, {img.shape[2]} canali)")
        return img

    def to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """Converte l'immagine in scala di grigi."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_blur(self, image: np.ndarray, ksize: int = 5, blur_type: str = "gaussian") -> np.ndarray:
        """Applica un filtro di sfocatura per riduzione rumore."""
        if ksize % 2 == 0:
            ksize += 1  # il kernel deve essere dispari
        if blur_type == "gaussian":
            return cv2.GaussianBlur(image, (ksize, ksize), 0)
        elif blur_type == "median":
            return cv2.medianBlur(image, ksize)
        else:
            return cv2.blur(image, (ksize, ksize))

    def detect_edges(self, image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
        """Rileva i bordi utilizzando l'algoritmo Canny."""
        gray = self.to_grayscale(image) if len(image.shape) == 3 else image
        blurred = self.apply_blur(gray, ksize=5)
        edges = cv2.Canny(blurred, threshold1, threshold2)
        return edges

    def apply_threshold(self, image: np.ndarray, method: str = "otsu") -> np.ndarray:
        """Binarizza l'immagine applicando una sogliatura (Thresholding)."""
        gray = self.to_grayscale(image) if len(image.shape) == 3 else image
        blurred = self.apply_blur(gray, ksize=5)

        if method == "otsu":
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif method == "adaptive":
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
        else:
            _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        return thresh

    def find_and_draw_contours(self, image: np.ndarray, min_area: float = 100.0) -> tuple[np.ndarray, list]:
        """
        Rileva i contorni dall'immagine ed evidenzia forme e bounding box.
        Ritorna l'immagine annotata e la lista delle informazioni sui contorni.
        """
        annotated = image.copy()
        gray = self.to_grayscale(image) if len(image.shape) == 3 else image
        blurred = self.apply_blur(gray, ksize=5)
        edges = cv2.Canny(blurred, 50, 150)

        # Trova contorni
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            if area < min_area:
                continue

            # Perimetro e approssimazione poligono
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            x, y, w, h = cv2.boundingRect(c)

            # Riconoscimento forma approssimata
            vertices = len(approx)
            if vertices == 3:
                shape_name = "Triangolo"
            elif vertices == 4:
                aspect_ratio = float(w) / h
                shape_name = "Quadrato" if 0.95 <= aspect_ratio <= 1.05 else "Rettangolo"
            elif vertices > 4:
                shape_name = "Cerchio/Poligono"
            else:
                shape_name = "Forma Irregolare"

            valid_contours.append({
                "id": i,
                "area": area,
                "perimeter": perimeter,
                "shape": shape_name,
                "bbox": (x, y, w, h)
            })

            # Disegna contorno in verde e bounding box in azzurro
            cv2.drawContours(annotated, [c], -1, (0, 255, 0), 2)
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 128, 0), 2)
            cv2.putText(annotated, f"{shape_name} ({int(area)}px)", (x, max(15, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        print(f"[+] Contorni rilevati: {len(valid_contours)} con area >= {min_area}px")
        return annotated, valid_contours

    def color_mask_hsv(self, image: np.ndarray, lower_hsv: list, upper_hsv: list) -> tuple[np.ndarray, np.ndarray]:
        """
        Filtra un intervallo di colori nello spazio colore HSV.
        lower_hsv: [H_min, S_min, V_min]
        upper_hsv: [H_max, S_max, V_max]
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array(lower_hsv, dtype="uint8")
        upper = np.array(upper_hsv, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
        filtered = cv2.bitwise_and(image, image, mask=mask)
        return mask, filtered

    def run_full_pipeline(self, image_path: str) -> dict:
        """Esegue l'intera pipeline di computer vision salvando tutti i passaggi intermedi."""
        image = self.load_image(image_path)
        base_name = Path(image_path).stem

        # 1. Grayscale
        gray = self.to_grayscale(image)
        gray_path = self.output_dir / f"{base_name}_1_gray.png"
        cv2.imwrite(str(gray_path), gray)

        # 2. Blur
        blurred = self.apply_blur(gray, ksize=5)
        blur_path = self.output_dir / f"{base_name}_2_blur.png"
        cv2.imwrite(str(blur_path), blurred)

        # 3. Canny Edges
        edges = self.detect_edges(image)
        edges_path = self.output_dir / f"{base_name}_3_edges.png"
        cv2.imwrite(str(edges_path), edges)

        # 4. Thresholding (Otsu)
        thresh = self.apply_threshold(image, method="otsu")
        thresh_path = self.output_dir / f"{base_name}_4_thresh.png"
        cv2.imwrite(str(thresh_path), thresh)

        # 5. Contorni e forme
        annotated, contours_info = self.find_and_draw_contours(image)
        contours_path = self.output_dir / f"{base_name}_5_contours.png"
        cv2.imwrite(str(contours_path), annotated)

        print("\n" + "="*50)
        print(f"[*] Pipeline completata con successo per: {image_path}")
        print(f"[*] Risultati salvati nella cartella: {self.output_dir.resolve()}")
        print(f"  1. Scala di grigi:    {gray_path.name}")
        print(f"  2. Riduzione rumore:  {blur_path.name}")
        print(f"  3. Rilevamento bordi: {edges_path.name}")
        print(f"  4. Binarizzazione:    {thresh_path.name}")
        print(f"  5. Contorni & forme:  {contours_path.name}")
        print("="*50)

        return {
            "original_shape": image.shape,
            "contours_count": len(contours_info),
            "files": {
                "gray": str(gray_path),
                "blur": str(blur_path),
                "edges": str(edges_path),
                "thresh": str(thresh_path),
                "contours": str(contours_path)
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Pipeline di Computer Vision classica con OpenCV")
    parser.add_argument("--image", type=str, default="avatar.png", help="Percorso dell'immagine da analizzare (default: avatar.png)")
    parser.add_argument("--edges", action="store_true", help="Esegui solo rilevamento bordi Canny")
    parser.add_argument("--contours", action="store_true", help="Esegui solo rilevamento contorni")
    parser.add_argument("--outdir", type=str, default="outputs/vision", help="Cartella di output")
    args = parser.parse_args()

    pipeline = OpenCVVisionPipeline(output_dir=args.outdir)

    if not os.path.exists(args.image):
        print(f"[!] Immagine {args.image} non trovata.")
        return

    if args.edges:
        img = pipeline.load_image(args.image)
        edges = pipeline.detect_edges(img)
        out = Path(args.outdir) / f"{Path(args.image).stem}_edges.png"
        cv2.imwrite(str(out), edges)
        print(f"[+] Bordi salvati in: {out}")
    elif args.contours:
        img = pipeline.load_image(args.image)
        annotated, info = pipeline.find_and_draw_contours(img)
        out = Path(args.outdir) / f"{Path(args.image).stem}_contours.png"
        cv2.imwrite(str(out), annotated)
        print(f"[+] Immagine con contorni salvata in: {out}")
    else:
        pipeline.run_full_pipeline(args.image)


if __name__ == "__main__":
    main()
