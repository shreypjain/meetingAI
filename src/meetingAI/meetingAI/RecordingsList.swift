//
//  RecordingsList.swift
//  meetingAI
//
//  Created by Shrey Jain on 7/9/20.
//  Copyright © 2020 Shrey Jain. All rights reserved.
//

import Foundation
import SwiftUI

struct RecordingsList: View {
    
    @ObservedObject var audioRecorder: AudioRecorder
    
    var body: some View {
        List {
            Text("Empty list")
        }
    }
}

struct RecordingsList_Previews: PreviewProvider {
    static var previews: some View {
        RecordingsList(audioRecorder: AudioRecorder())
    }
}
